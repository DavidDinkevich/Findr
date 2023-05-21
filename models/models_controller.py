import multiprocessing
import signal

from preprocessing import compress_video, remap_results_to_original_video
import time
import os
from model_server import start_server, get_next_query, send_response
import yolo.yolov5.yolov5_engine as yolov5
from clip_ import clip_engine
from efficientnet import efficientnet_engine
from resnet import resnet_engine
from inceptionv3 import inceptionv3_engine

model_module_map = {
    'yolov5': yolov5,
    'clip': clip_engine,
    'efficientnet': efficientnet_engine,
    'resnet': resnet_engine,
    'inceptionv3': inceptionv3_engine
}
# To store process objects for the models
model_procs = {}
# To store the current query (query is unfortunately duplicated for each model)
current_query_queue = multiprocessing.Queue()
# To store model results
model_response_queue = multiprocessing.Queue()


# Loads all of the models
def load_models():
    for model_name in model_module_map:
        # Create process
        proc = multiprocessing.Process(
            target=model_process_worker,
            args=(model_name, current_query_queue, model_response_queue)
        )
        proc.start()
        model_procs[model_name] = proc


# Runs the model with the given name and returns a process object
def model_process_worker(model_name, current_query_queue, model_response_queue):
    # Load the model from memory
    model_module_map[model_name].load_model()

    while True:
        req = current_query_queue.get(block=True) # Get query from queue
        if req is None:
            break
        # Only deal with requests for this model
        if model_name not in req['models']:
            # Add element back
            current_query_queue.put(req)
            continue
        # Process and add response to response queue
        resp = model_module_map[model_name].process_query(req)
        # Add name of model
        resp = { model_name: resp }
        model_response_queue.put(resp)


def handle_queries():
    while True:
        # Get next query
        query = get_next_query()
        # Process
        resp = process_query(query)
        # Send back response
        send_response(resp)


# Process a single query
def process_query(query_dict):
    print(f'[MODEL CONTROLLER]: Beginning to process query id={query_dict["id"]}')
    start = time.time()

    # Compress the video
    print('[MODEL CONTROLLER]: Compressing video...')
    compression_start = time.time()
    compressed_name = f'compressed_{os.path.basename(query_dict["video_path"])}'
    reconstruction_map = compress_video(
        input_file=query_dict["video_path"],
        output_file=compressed_name,
        similarity_threshold=0.9
    )
    # Replace video_path in query with compressed path instead
    query_dict['video_path'] = compressed_name
    print(f'[MODEL CONTROLLER]: Finished compressing video. Time elapsed: {time.time() - compression_start}')

    # Add query to query queue. We have to add a copy for each model (weird implementation, I know...)
    # but it's simpler than using mutexes
    for i in range(len(query_dict['models'])):
        specific_query = query_dict.copy()
        specific_query['models'] = [query_dict['models'][i]]
        current_query_queue.put(specific_query)
        print(f'[MODEL CONTROLLER]: added query: {specific_query}')
    print(f'[MODEL CONTROLLER]: sending request {query_dict["id"]}')

    # Create response
    response = { 'id': query_dict['id'] }

    # Pull responses from response queue (num responses = num models requested in query)
    for i in range(len(query_dict['models'])):
        # Pull a response from the queue
        resp = model_response_queue.get(block=True) # Block if necessary
        # Reconstruct intervals from response to original video
        model_name = list(resp.keys())[0]
        matches = resp[model_name]
        resp[model_name] = remap_results_to_original_video(model_name, matches, reconstruction_map)
        response.update(resp) # Add
        print(f'[MODEL CONTROLLER]: got response for #{query_dict["id"]}: {resp}')

    print(f'[MODEL CONTROLLER]: Query: {query_dict["id"]} finished. Response: {response}\nTotal time elapsed: {time.time() - start}')

    return response


if __name__ == "__main__":
    # MAKE SURE CHILD PROCS ARE TERMINATED ON EXIT
    # Define a signal handler to terminate child processes
    def sigterm_handler(signum, frame):
        for process in multiprocessing.active_children():
            process.terminate()
        exit(0)
    # Register the signal handler
    signal.signal(signal.SIGTERM, sigterm_handler)

    # ROUTINE
    start_server()
    load_models()
    handle_queries()


import multiprocessing
import threading
import os
import signal

from preprocessing import compress_video, reconstruct_and_write_original_intervals
import subprocess
import time
import os
import json
from model_server import start_server, get_next_query, send_response
import yolo.yolov5.yolov5_engine as yolov5

# Maps model name to its respective engine file
model_engine_paths = {
    # 'clip': './clip/clip_engine.py',
    'yolov5': './yolo/yolov5/yolov5_engine.py',
    # 'yolov7': './yolo/yolov7/yolov7_engine.py'
}
model_module_map = {
    'yolov5': yolov5,
}
# To store process objects for the models
model_procs = {}
# To store the current query (query is unfortunately duplicated for each model)
current_query_queue = multiprocessing.Queue()
# To store model results
model_response_queue = multiprocessing.Queue()


# Loads all of the models
def load_models():
    for model_name in model_engine_paths:
        # Create process
        proc = multiprocessing.Process(
            target=model_process_worker,
            args=(model_name, current_query_queue, model_response_queue)
        )
        proc.start()
        model_procs[model_name] = proc
        return proc


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
    print(f'Beginning to process query id={query_dict["id"]}')
    start = time.time()

    # Compress the video
    print('Compressing video...')
    compression_start = time.time()
    compressed_name = f'compressed_{os.path.basename(query_dict["video_path"])}'
    reconstruction_map = compress_video(
        input_file=query_dict["video_path"],
        output_file=compressed_name,
        similarity_threshold=0.9
    )
    print(f'Finished compressing video. Time elapsed: {time.time() - compression_start}')

    # Add query to query queue. We have to add a copy for each model (weird implementation, I know...)
    # but it's simpler than using mutexes
    for i in range(len(query_dict['models'])):
        current_query_queue.put(query_dict)
    print(f'MC: sending request #{query_dict["id"]}')

    current_query = None # Query has been sent to all models
    # Create response
    response = { 'id': query_dict['id'] }

    # Pull responses from response queue (num responses = num models requested in query)
    for i in range(len(query_dict['models'])):
        # Pull a response from the queue
        resp = model_response_queue.get(block=True) # Block if necessary
        response.update(resp) # Add
        print(f'MC: got response for #{query_dict["id"]}: {resp}')

    print(f'Query: {query_dict["id"]} finished. Total time elapsed: {time.time() - start}')

    return response


if __name__ == "__main__":

    # ROUTINE
    load_models()
    start_server()
    handle_queries()


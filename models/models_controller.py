from preprocessing import compress_video, reconstruct_and_write_original_intervals
import subprocess
import time
import os
import json
from model_server import start_server, get_next_query, send_response


# Maps model name to its respective engine file
model_engine_paths = {
    'clip': './clip/clip_engine.py',
    'yolov5': './yolo/yolov5/yolov5_engine.py',
    'yolov7': './yolo/yolov7/yolov7_engine.py'
}


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

    # Run models
    procs = {}
    for model_name in query_dict['models']:
        proc = run_model(model_name, query_dict['query'], compressed_name)
        procs[model_name] = proc

    # Wait for subprocesses
    for model_name in procs:
        procs[model_name].wait()
        # Check if model succeeded
        return_code = procs[model_name].returncode
        if return_code != 0:
            print(f'Model {model_name} CRASHED with exit code: {return_code}')

    response = { 'id': query_dict['id'] }

    # Reconstruct intervals for original video
    for model_name in query_dict['models']:
        # Skip procs that failed
        if procs[model_name].returncode != 0:
            continue
        if 'clip' in model_name:
            model_type = 'clip'
        elif 'yolo' in model_name:
            model_type = 'yolo'
        else:
            raise NotImplementedError("Haven't implemented models other than yolo and clip")

        output_file = f'{model_name}_results.json'
        reconstruct_and_write_original_intervals(model_type, output_file, reconstruction_map)

        with open(output_file, 'r') as f:
            response[model_name] = json.load(f)

    print(f'Query: {query_dict["id"]} finished. Total time elapsed: {time.time() - start}')

    return response



# Runs the model with the given name and returns a process object
def run_model(model_name, query, source):
    print(f'Starting {model_name}...')
    output_file = f'{model_name}_results.json'
    proc_name = model_engine_paths[model_name]
    proc = subprocess.Popen(
        ['python', proc_name, '--source', source, '--query', query, '--o', output_file])
    return proc


if __name__ == "__main__":
    start_server()
    handle_queries()


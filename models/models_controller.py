from preprocessing import compress_video, reconstruct_and_write_original_intervals
import subprocess
import time
import os


model_engine_paths = {
    'clip': './clip/clip_engine.py',
    'yolov5': './yolo/yolov5/yolov5_engine.py',
    'yolov7': './yolo/yolov7/yolov7_engine.py'
}


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
    procs = []
    for model_name in query_dict['models']:
        proc = run_model(model_name, query_dict['query'], compressed_name)
        procs.append(proc)

    # Wait for subprocesses
    for proc in procs:
        proc.wait()

    # Reconstruct intervals for original video
    for model_name in query_dict['models']:
        if 'clip' in model_name:
            model_type = 'clip'
        elif 'yolo' in model_name:
            model_type = 'yolo'
        else:
            raise NotImplementedError("Haven't implemented models other than yolo and clip")

        output_file = f'{model_name}_results.json'
        reconstruct_and_write_original_intervals(model_type, output_file, reconstruction_map)

    print(f'Query: {query_dict["id"]} finished. Total time elapsed: {time.time() - start}')


def run_model(model_name, query, source):
    print(f'Starting {model_name}...')
    output_file = f'{model_name}_results.json'
    proc_name = model_engine_paths[model_name]
    proc = subprocess.Popen(
        ['python', proc_name, '--source', source, '--query', query, '--o', output_file])
    return proc


if __name__ == "__main__":
    start = time.time()

    query1 = {
        'id': '1234',
        'query': 'giraffe',
        'video_path': './resources/giraffe_and_hippo.mp4',
        'models': ['yolov7']
        # 'models': ['clip', 'yolov5']
    }
    query2 = {
        'id': '5678',
        'query': 'hippo',
        'video_path': './resources/hippo.mp4',
        'models': ['yolov7', 'yolov5']
    }

    process_query(query1)
    # process_query(query2)

    print(f'Total time elapsed: {time.time() - start}')



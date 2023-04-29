from preprocessing import compress_video, reconstruct_and_write_original_intervals
import subprocess
import time
import json
import argparse


def run_model(model_name, query, source):
    print(f'Starting {model_name}...')
    output_file = f'{model_name}_results.json'
    proc_name = f'{model_name}_engine.py'
    proc = subprocess.Popen(
        ['python', proc_name, '--source', source, '--query', query, '--o', output_file])
    return proc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='source')
    parser.add_argument('--query', type=str, help='query')
    opt = parser.parse_args()

    start = time.time()

    # Compress the video
    print('Compressing video...')
    compression_start = time.time()
    compressed_name = f'compressed_{opt.source}'
    reconstruction_map = compress_video(
            input_file=opt.source, output_file=compressed_name, similarity_threshold=0.9)
    print(f'Finished compressing video. Time elapsed: {time.time() - compression_start}')

    # Run models
    procs = [
        run_model('clip', opt.query, compressed_name),
        run_model('yolo', opt.query, compressed_name),
        run_model('yolov5', opt.query, compressed_name)
    ]

    # Wait for subprocesses
    for proc in procs:
        proc.wait()

    # Reconstruct intervals for original video
    reconstruct_and_write_original_intervals('CLIP', 'clip_results.json', reconstruction_map)
    reconstruct_and_write_original_intervals('YOLO', 'yolo_results.json', reconstruction_map)
    reconstruct_and_write_original_intervals('YOLO', 'yolov5_results.json', reconstruction_map)

    print(f'Total time elapsed: {time.time() - start}')



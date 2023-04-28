from preprocessing import compress_video, remap_results_to_original_video
import subprocess
import time
import json
import argparse


def reconstruct_and_write_original_intervals(model, intervals_file, reconstruction_map):
    with open(intervals_file, 'r+') as f:
        intervals = json.load(f)
        reconstructed_intervals = remap_results_to_original_video(model, intervals, reconstruction_map)
        f.seek(0)
        f.truncate()
        json.dump(reconstructed_intervals, f)


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

    # Run CLIP in subprocess
    print(f'Starting CLIP...')
    clip_results_json = 'clip_results.json'
    clip_proc = subprocess.Popen(
        ['python', 'clip_engine.py', '--source', compressed_name, '--query', opt.query, '--o', clip_results_json])

    # Run YOLOv7 in subprocess
    print(f'Starting YOLOv7...')
    yolo_results_json = 'yolo_results.json'
    yolo_proc = subprocess.Popen(
        ['python', 'yolo_engine.py', '--source', compressed_name, '--query', opt.query, '--o', yolo_results_json])

    # Run YOLOv5 in subprocess
    print(f'Starting YOLOv5...')
    yolov5_results_json = 'yolov5_results.json'
    yolov5_proc = subprocess.Popen(
        ['python', 'yolov5_engine.py', '--source', compressed_name, '--query', opt.query, '--o', yolov5_results_json])

    # Wait for subprocesses
    clip_proc.wait()
    yolo_proc.wait()
    yolov5_proc.wait()

    # Reconstruct intervals for original video
    reconstruct_and_write_original_intervals('CLIP', clip_results_json, reconstruction_map)
    reconstruct_and_write_original_intervals('YOLO', yolo_results_json, reconstruction_map)
    reconstruct_and_write_original_intervals('YOLO', yolov5_results_json, reconstruction_map)

    print(f'Total time elapsed: {time.time() - start}')



import subprocess
from preprocessing import compress_video
import time
import os

if __name__ == "__main__":
    input_video = 'giraffe_and_hippo.mp4'
    query = 'a giraffe eating'

    start = time.time()

    # Compress the video
    compressed_name = f'compressed_{input_video}'
    reconstruction_map = compress_video(input_video, output_file=compressed_name, similarity_threshold=0.9, skip_rate=3)
    print(reconstruction_map)

    # Run CLIP in subprocess
    print(f'making clip process: {time.time()}')
    clip_results_json = f'clip_results_{os.getpid()}.json'
    clip_proc = subprocess.Popen(f'python clip_engine.py {compressed_name} {query} -o {clip_results_json}'.split())

    # Run YOLO in subprocess
    print(f'making yolo process: {time.time()}')
    yolo_results_json = f'yolo_results_{os.getpid()}.json'
    yolo_proc = subprocess.Popen(f'python yolo_engine.py --source {compressed_name}'.split())

    # Wait for subprocesses
    clip_proc.wait()
    yolo_proc.wait()

    # Cleanup
    # os.remove(clip_results_json)
    # os.remove(yolo_results_json)

    print(f'done in {time.time() - start}')


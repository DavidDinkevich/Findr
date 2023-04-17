import subprocess
from preprocessing import compress_video
import time
import os

if __name__ == "__main__":
    input_video = 'giraffe_and_hippo.mp4'
    query = 'giraffe'

    start = time.time()

    # Compress the video
    compressed_name = f'compressed_{input_video}'
    compress_video(input_video, output_file=compressed_name, similarity_threshold=0.9, skip_rate=3)

    # Run CLIP in subprocess
    print(f'making clip process: {time.time()}')
    clip_results_name = f'clip_results_{os.getpid()}.json'
    clip_proc = subprocess.Popen(f'python clip_engine.py {compressed_name} {query} -o {clip_results_name}'.split(' '))

    # Run YOLO in subprocess
    print(f'making yolo process: {time.time()}')
    yolo_results_name = f'yolo_results_{os.getpid()}.json'
    yolo_proc = subprocess.Popen(f'python .\yolov7\detect.py --weights .\yolov7\yolov7-e6e.pt --source {compressed_name} --nosave --save-txt --save-conf'.split(' '))

    # Wait for subprocesses
    clip_proc.wait()
    yolo_proc.wait()

    print(f'done in {time.time() - start}')


import argparse
import subprocess
import json
import time
import numpy as np


def filter_with_query(query, matches):
    filtered_matches = []
    for frame_json in matches:
        matches = frame_json['matches']
        filtered = [match for match in matches if match['label'] in query]
        if len(filtered) > 0:
            filtered_matches.append({
                'frame_index': frame_json['frame_index'],
                'matches': filtered
            })
    return filtered_matches

def add_average_accuracy_to_matches(matches):
    for frame_json in matches:
        accuracies = [match['accuracy'] for match in frame_json['matches']]
        frame_json['accuracy'] = np.array(accuracies).mean()

if __name__ == '__main__':
    yolo_start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='source')
    parser.add_argument('--query', type=str, help='query')  # file/folder, 0 for webcam
    parser.add_argument('--o', type=str, help='output json')
    opt = parser.parse_args()

    # File to store output
    results_json = opt.o

    # Run yolo
    subprocess.call(
        ['python', '.\yolov7\detect.py', '--weights', '.\yolov7\yolov7-e6e.pt', '--source', opt.source,
                '--json_output_path', results_json, '--nosave', '--save-txt', '--save-conf'])

    # Read compressed matches json and filter with query
    with open(results_json, 'r') as f:
        compressed_matches = json.load(f)

    # Keep matches that relate to query, and overall frame accuracy for each frame
    filtered_compressed_matches = filter_with_query(opt.query, compressed_matches)
    add_average_accuracy_to_matches(filtered_compressed_matches)

    # Write to file (replace the file yolo used)
    with open(results_json, 'w') as f:
        json.dump(filtered_compressed_matches, f)

    print(f'YOLO terminated. Time elapsed: {time.time() - yolo_start}')


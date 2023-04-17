import argparse
import subprocess
import json
import os
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--query', type=str, help='source')  # file/folder, 0 for webcam
    opt = parser.parse_args()

    # Run yolo
    compressed_matches_json = 'compressed_matches.json'
    subprocess.call(f'python .\yolov7\detect.py --weights .\yolov7\yolov7-e6e.pt --source {opt.source} --json_output_path {compressed_matches_json} --nosave --save-txt --save-conf'.split())

    # Read compressed matches json and filter with query
    with open(compressed_matches_json, 'r') as f:
        compressed_matches = json.load(f)

    # Keep matches that relate to query, and overall frame accuracy for each frame
    filtered_compressed_matches = filter_with_query(opt.query, compressed_matches)
    add_average_accuracy_to_matches(filtered_compressed_matches)

    # Write to file (replace the file yolo used)
    with open(compressed_matches_json, 'w') as f:
        json.dump(filtered_compressed_matches, f)


    print('done with yolo')

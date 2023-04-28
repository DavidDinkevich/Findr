import argparse
import json
import time
import numpy as np
import torch
import cv2

device = None
model = None

def load_yolo(version='yolov5'):
    print('Loading yolo...')
    t1 = time.time()
    if version == 'yolov5':
        global device, model
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {device}')
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)
        model.eval()
        print(f'YOLO: finished loading. Time elapsed: {time.time() - t1}')


def run_yolo(input_path):
    global model
    # Open video file
    cap = cv2.VideoCapture(input_path)

    matched_frames = []
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # print(f'Frame index: {frame_index}/{n_frames}')

        # Apply YOLO detection to the frame
        results = model(frame)

        # Loop through each detection and print out its label and confidence score
        frame_match = {'frame_index': frame_index, 'matches': []}
        for detection in results.xyxy[0]:
            # ADD MATCH
            frame_match['matches'].append({
                'label': model.names[int(detection[-1])],
                'accuracy': float(f'{detection[-2]:.2f}')
            })

        # Add this frame to list of matches
        if len(frame_match['matches']) > 0:  # If no matches for this frame, skip
            matched_frames.append(frame_match)

        frame_index += 1

    # Release the video file and close the windows
    cap.release()
    return matched_frames


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
    load_yolo(version='yolov5')
    matched_frames = run_yolo(opt.source)
    # Write matched frames structure to file in JSON
    with open(results_json, 'w') as f:
        json.dump(matched_frames, f)


    # Read compressed matches json and filter with query
    with open(results_json, 'r') as f:
        compressed_matches = json.load(f)

    # Keep matches that relate to query, and overall frame accuracy for each frame
    filtered_compressed_matches = filter_with_query(opt.query, compressed_matches)
    add_average_accuracy_to_matches(filtered_compressed_matches)

    # Write to file (replace the file yolo used)
    with open(results_json, 'w') as f:
        json.dump(filtered_compressed_matches, f)

    print(f'YOLOv5 terminated. Time elapsed: {time.time() - yolo_start}')


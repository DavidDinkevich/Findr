import time
import argparse
import json
import torch
import clip
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import utils

clip_start = time.time()

# LOAD CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
print('Using device: ', device)
model, preprocess = clip.load("ViT-B/32", device=device)
print('Finished loading CLIP')

def compute_similarity(query, frame):
    # Convert opencv frame to PIL image (what CLIP uses)
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = preprocess(pil_image).unsqueeze(0).to(device)
    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        # Encode image and query to common semantic space using model
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        # Compute similarity using dot product
        dot = (100.0 * image_features @ text_features.T).squeeze()
        similarity = dot / (image_features.norm(dim=1) * text_features.norm(dim=1))

    return similarity.cpu().numpy()


def compute_frame_similarities(filename, query):
    cap = cv2.VideoCapture(filename)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    similarities = []

    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret: # haven't reached the end yet
            break

        # Compute similarity
        similarity = compute_similarity(query, frame)
        similarities.append(similarity.item())

        frame_index += 1
        # print(f"Frame number {frame_index}/{total_frames}", end="\r", flush=True)
        # print(f"Frame number {frame_index}/{total_frames}")

    cap.release() # Release resources
    return similarities


def compute_accuracy_classes(similarities, method='dbscan'):
    labels = None
    if method == 'dbscan':
        # Run DBSCAN
        dbscan = DBSCAN(eps=2, min_samples=2)
        labels = dbscan.fit_predict(similarities)
        # We want the labels are 0 to #clusters-1, but dbscan assigns -1 for "noise points"
        # We'll treat noise points as additional clusters
        new_cluster_label = len(set(labels)) - 1
        for i in range(len(labels)):
            if labels[i] == -1:
                labels[i] = new_cluster_label
                new_cluster_label += 1

    # For now on, we want similarities to be standard np array
    similarities = similarities.reshape((-1,))

    # Create an array of tuples: (avg_acc, [frame_indices]) for each cluster
    accuracy_classes = []
    for label in range(len(set(labels))):
        # Compute the frame indices in the accuracy class
        frame_indices_in_acc_class = [i for i in range(len(similarities)) if labels[i] == label]
        # Compute the mean class accuracy
        avg_acc_in_class = np.take(similarities, frame_indices_in_acc_class).mean()
        # Merge the intervals in the accuracy class
        intervals = [(n, n) for n in frame_indices_in_acc_class]
        intervals = utils.merge_contiguous_tuples(intervals)

        # print(f'{avg_acc_in_class}:  {str(intervals)}')
        accuracy_classes.append({
            'accuracy': avg_acc_in_class,
            'intervals': intervals
        })
    return accuracy_classes

# TODO TEST OPTIMIZATION
def merge_contiguous_intervals(accuracy_classes):
    new_acc_classes = []
    for frame_entry in accuracy_classes:
        frame_entry['intervals'] = utils.merge_contiguous_tuples(frame_entry['intervals'])
    return new_acc_classes


if __name__ == '__main__':
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process video data and create a transcript.')

    # Add arguments to the parser
    parser.add_argument('--source', type=str, help='path to the video file')
    parser.add_argument('--query', type=str, help='query to search for in the video')
    parser.add_argument('--o', '--json_output_path', type=str, default='clip_results.txt', help='json output file path')
    parser.add_argument('--p', '--plot_results', action='store_true', help='whether to plot the results')

    # Parse the arguments
    args = parser.parse_args()
    json_output_path = args.o
    plot_results = args.p

    # MAIN MODEL BEHAVIOR

    # Get frames and compute the similarities for each
    frame_similarities = compute_frame_similarities(args.source, args.query)
    frame_similarities = np.array(frame_similarities).reshape(-1,1) # Reshape as column vec for later

    # Compute accuracy classes
    accuracy_classes = compute_accuracy_classes(frame_similarities)

    # Write accuracy classes to file in JSON
    with open(json_output_path, 'w') as f:
        json.dump(accuracy_classes, f)

    if plot_results:
        # Set up the figure
        fig, ax = plt.subplots()

        # Plot each array of ints as lines in a different color
        for i, frame_entry in enumerate(accuracy_classes):
            for segment in frame_entry['intervals']:
                start, end = segment[0], segment[1] + 1
                acc = frame_entry['accuracy']
                ax.plot([start, end], [acc, acc], c=f'C{i}')

        # Set the x and y axis labels
        plt.xlabel('Video Frames')
        plt.ylabel('Match Confidence')
        plt.title(args.query)

        # Show the plot
        plt.show()

    print(f'CLIP terminated. Time elapsed: {time.time() - clip_start}')


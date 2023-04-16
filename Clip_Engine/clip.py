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

# LOAD CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
print('Using device: ', device)
model, preprocess = clip.load("ViT-B/32", device=device)
print('Finished loading model')

def compute_similarity(query, frame):
    # Convert opencv frame to PIL image (what CLIP uses)
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = preprocess(pil_image).unsqueeze(0).to(device)
    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1)

        # Compute similarity using dot product
        dot = (100.0 * image_features @ text_features.T).squeeze()
        similarity = dot / (image_features.norm(dim=1) * text_features.norm(dim=1))

    return similarity.cpu().numpy()


def compute_frame_similarities(filename, query):
    cap = cv2.VideoCapture(filename)
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
        print(f"Frame number {frame_index}/105", end="\r", flush=True)

    print('num frames: ', frame_index + 1)
    cap.release() # Release resources
    return similarities


def compute_accuracy_classes(similarities, method='dbscan'):
    labels = None
    if method == 'dbscan':
        # Run DBSCAN
        dbscan = DBSCAN(eps=2, min_samples=2)
        # Labels are 0 to #clusters-1
        labels = dbscan.fit_predict(similarities)

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
        accuracy_classes.append((avg_acc_in_class, intervals))
    return accuracy_classes


def merge_contiguous_intervals(accuracy_classes):
    new_acc_classes = []
    for (acc, intervals) in accuracy_classes:
        merged_intervals = utils.merge_contiguous_tuples(intervals)
        new_acc_classes.append((acc, merged_intervals))
    return new_acc_classes


if __name__ == '__main__':
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process video data and create a transcript.')

    # Add arguments to the parser
    parser.add_argument('video_path', type=str, help='path to the video file')
    parser.add_argument('query', type=str, help='query to search for in the video')
    parser.add_argument('-o', '--json_output_path', type=str, default='clip_results.txt', help='json output file path')
    parser.add_argument('-p', '--plot_results', action='store_true', help='whether to plot the results')

    # Parse the arguments
    args = parser.parse_args()

    # MAIN MODEL BEHAVIOR

    # Get frames and compute the similarities for each
    frame_similarities = compute_frame_similarities(args.video_path, args.query)
    frame_similarities = np.array(frame_similarities).reshape(-1,1) # Reshape as column vec for later

    # Compute accuracy classes
    accuracy_classes = compute_accuracy_classes(frame_similarities)

    # Write accuracy classes to file in JSON
    with open(args.json_output_path, 'w') as f:
        json.dump(accuracy_classes, f)

    if args.plot_results:
        # Set up the figure
        fig, ax = plt.subplots()

        # Plot each array of ints as lines in a different color
        for i, (x, y) in enumerate(accuracy_classes):
            for segment in y:
                start, end = segment[0], segment[1] + 1
                ax.plot([start, end], [x, x], c=f'C{i}')

        # Set the x and y axis labels
        plt.xlabel('Video Frames')
        plt.ylabel('Match Confidence')
        plt.title(args.query)

        # Show the plot
        plt.show()



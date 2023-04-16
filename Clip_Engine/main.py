import torch
import clip
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
import utils

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
        similarities.append((frame_index, similarity.item()))

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
        frame_indices_in_acc_class = [(i,) for i in range(len(similarities)) if labels[i] == label]
        avg_acc_in_class = np.take(similarities, frame_indices_in_acc_class).mean()

        # print(f'{avg_acc_in_class}:  {str(frame_indices_in_acc_class)}')
        accuracy_classes.append((avg_acc_in_class, frame_indices_in_acc_class))
    return accuracy_classes

        # Example
        # [1,0,1]
        # [(0,0.2),(1,0.9),(2,0.3)]
        # Result: [ (0.25, [0,2]), (0.9, [1]) ]


def merge_contiguous_intervals(accuracy_classes):
    new_acc_classes = []
    for (acc, intervals) in accuracy_classes:
        intervals = [(x,x) for (x,) in intervals] # TODO: DELETE!!!
        merged_intervals = utils.merge_contiguous_tuples(intervals)
        new_acc_classes.append((acc, merged_intervals))
    return new_acc_classes


if __name__ == '__main__':
    # Load video frames
    video = 'giraffe_and_hippo.mp4'
    query = 'a giraffe'
    # hippo: 15 to 87

    # Get frames
    frames_and_similarities = compute_frame_similarities(video, query)
    similarities = np.array([t[1] for t in frames_and_similarities]).reshape(-1, 1)

    # Compute accuracy classes
    accuracy_classes = compute_accuracy_classes(similarities)
    accuracy_classes = merge_contiguous_intervals(accuracy_classes)

    # Set up the figure
    fig, ax = plt.subplots()

    # Plot each array of ints as lines in a different color
    for i, (x, y) in enumerate(accuracy_classes):
        for segment in y:
            if len(segment) == 2:
                start, end = segment
            else:
                start, end = segment[0], segment[0] + 1
            ax.plot([start, end], [x, x], c=f'C{i}')

    # Set the x and y axis labels
    plt.xlabel('Video Frames')
    plt.ylabel('Match Confidence')
    plt.title(query)

    # Show the plot
    plt.show()

# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('all-MiniLM-L6-v2')
#
# #Our sentences we like to encode
# sentences = ['This framework generates embeddings for each input sentence',
#     'Sentences are passed as a list of string.',
#     'The quick brown fox jumps over the lazy dog.']
#
# #Sentences are encoded by calling model.encode()
# embeddings = model.encode(sentences)
#
# #Print the embeddings
# for sentence, embedding in zip(sentences, embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", embedding)
#     print("")



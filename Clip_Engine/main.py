import torch
import clip
from PIL import Image
import cv2
import numpy as np

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
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        probs = np.around(probs, decimals=4)

        # Compute similarity using dot product
        similarity = (100.0 * image_features @ text_features.T).squeeze()

    return similarity
    # # print("Label probs:", probs)  # prints: [[0.9927937  0.00421068 0.00299572]]
    # print('similarity:', probs[0][0])
    # return probs[0][0]


def find_matched_frames(filename, query, similarity_threshold):
    cap = cv2.VideoCapture(filename)
    matched_frames = []

    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret: # haven't reached the end yet
            break

        # Compute similarity
        similarity = compute_similarity(query, frame)

        if similarity > similarity_threshold:
            print(f'Similarity {similarity} - match')
            matched_frames.append((frame_index, similarity))
        else:
            print(f'Similarity {similarity} - no match')

        frame_index += 1

    print('num frames: ', frame_index + 1)
    cap.release() # Release resources
    return matched_frames

if __name__ == '__main__':
    # Load video frames
    video = 'giraffe_and_hippo.mp4'
    query = 'giraffe'
    matched_frames = find_matched_frames(video, query, similarity_threshold=2200)
    print(matched_frames)

    # hippo: 15 to 87
    # giraffe






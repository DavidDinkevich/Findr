import time
import cv2
import torch
from torchvision.models import inception_v3
from torchvision.transforms import transforms
from PIL import Image
from imagenet_utils import imagenet_classes


# Globals
device = None
model = None


def load_model():
    print('[INCEPTIONV3] Loading...')
    t1 = time.time()
    global model, device
    # Choose device
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'
    # Load the pretrained EfficientNet model
    model = inception_v3(pretrained=True).to(device)
    model.eval()
    print(f'[INCEPTIONV3]: finished loading. Time elapsed: {time.time() - t1}')


def process_query(query_dict):
    # Unpack query
    query = query_dict['query']
    video_path = query_dict['video_path']
    print(f'[INCEPTIONV3]: got query: {query_dict}')

    # Write matched frames structure to file in JSON
    matched_frames = run_efficientnet_on_video(query, video_path)

    print(f'[INCEPTIONV3]: sending response: {matched_frames}\n')
    return matched_frames


def run_efficientnet_on_video(query, input_path):
    global model
    # Open video file
    cap = cv2.VideoCapture(input_path)

    matched_frames = []
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess function to transform the image
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = preprocess(frame).unsqueeze(0).to(device)

        # Run inference on the preprocessed frame
        with torch.no_grad():
            outputs = model(frame).cpu()

        # Get the predicted class
        softmax_scores = torch.softmax(outputs, dim=1)
        # print(f'Outputs: {outputs}, shape={outputs.shape}')
        predicted_class_index = torch.argmax(outputs)
        predicted_class = imagenet_classes[predicted_class_index]
        acc = f'{softmax_scores[0][predicted_class_index] * 100:.2f}'

        # Add this frame to list of matches (if significant)
        if is_significant_match(query, predicted_class):
            # Loop through each detection and print out its label and confidence score
            frame_match = {'frame_index': frame_index, 'accuracy': acc}
            matched_frames.append(frame_match)

        frame_index += 1

    # Release the video file and close the windows
    cap.release()
    return matched_frames


def is_significant_match(query, predicted_class):
    return predicted_class in query or query in predicted_class

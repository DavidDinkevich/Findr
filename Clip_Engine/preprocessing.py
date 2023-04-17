import cv2
import numpy as np

def _get_significant_frames(filename, similarity_threshold, skip_rate):
    cap = cv2.VideoCapture(filename)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    original_video_shape = None # Will update this after reading first frame
    significant_frames = []

    frame_index = 0
    curr_model_frame = None
    while True:
        ret = cap.grab()
        if not ret: # haven't reached the end yet
            break
        # Skip frames
        if frame_index % skip_rate != 0:
            frame_index += 1
            continue

        _, frame = cap.retrieve() # Decode
        print(f"Frame number {frame_index}/{total_frames}")

        if frame_index == 0: # First frame
            # Store original video shape
            original_video_shape = frame.shape
            # Update model frame: first convert frame to grayscale, then flatten
            curr_model_frame = frame.flatten().astype('float')
            print('NEW MODEL')
            significant_frames.append(frame)
        else: # Compute similarity between this frame and the model frame

            # Convert frame to grayscale and flatten
            processed_frame = frame.flatten().astype('float')

            # Compute cosine similarity between the two frames
            sim = np.dot(curr_model_frame, processed_frame) / (np.linalg.norm(curr_model_frame) * np.linalg.norm(processed_frame))
            print(f'Similarity is: {sim}')
            if sim < similarity_threshold:
                # Update model frame: first convert frame to grayscale, then flatten
                curr_model_frame = frame.flatten().astype('float')
                significant_frames.append(frame)

        frame_index += 1

    print(f'Num kept: {len(significant_frames)}')
    cap.release() # Release resources
    return significant_frames, fps, width, height


def _create_compressed_video(significant_frames, output_filename, fps, width, height):
    # Define output video properties
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    # Write significant frames to file
    for frame in significant_frames:
        out.write(frame)
    # Release resources
    out.release()


def compress_video(input_file, output_file, similarity_threshold=0.9, skip_rate=3):
    import time
    sig_frames, fps, w, h = _get_significant_frames(input_file, similarity_threshold=0.9, skip_rate=3)
    _create_compressed_video(sig_frames, output_file, fps, w, h)
    start = time.time()
    end = time.time()
    print(end - start)


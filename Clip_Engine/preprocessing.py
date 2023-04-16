import cv2
import numpy as np

def get_significant_frames(filename):
    cap = cv2.VideoCapture(filename)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    original_video_shape = None # Will update this after reading first frame
    significant_frames = []

    frame_index = 0
    curr_model_frame = None
    num_kept = 0
    while True:
        ret, frame = cap.read()
        print(f"Frame number {frame_index}/{total_frames}")

        if not ret: # haven't reached the end yet
            break

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
            if sim >= 0.9:
                print('dropped')
            else:
                print('kept -- NEW MODEL')


                num_kept += 1
                # Update model frame: first convert frame to grayscale, then flatten
                curr_model_frame = frame.flatten().astype('float')
                significant_frames.append(frame)

        frame_index += 1

    print(f'Num kept: {num_kept}')
    cap.release() # Release resources
    return significant_frames, fps, width, height


def create_compressed_video(significant_frames, output_filename, fps, width, height):
    # Define output video properties
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    # Write significant frames to file
    for frame in significant_frames:
        out.write(frame)
    # Release resources
    out.release()


if __name__ == '__main__':
    sig_frames, fps, w, h = get_significant_frames('giraffe_and_hippo.mp4')
    create_compressed_video(sig_frames, 'compressed_video.mp4', fps, w, h)


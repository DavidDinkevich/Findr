

import cv2

def load_video_frames(filename):
    cap = cv2.VideoCapture(filename)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frames.append(frame)

    cap.release()

    return frames


if __name__ == '__main__':
    frames = load_video_frames('giraffe.mp4')
    print(frames[0])

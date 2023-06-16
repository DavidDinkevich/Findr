import cv2
import numpy as np
import threading
import time
import multiprocessing


def compress_video(input_file, output_file, similarity_threshold=0.9):
    # Open video
    cap = cv2.VideoCapture(input_file)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # COMPUTE NUMBER OF THREADS AND SKIP RATE
    # Rather arbitrary...
    n_threads = 1 if n_frames < 1000 else int(multiprocessing.cpu_count() / 2)
    skip_rate = 1 if n_frames < 100 else int(round(0.0008 * n_frames + 3))

    print(f'Num frames: {n_frames}')
    print(f'Num threads: {n_threads}')
    print(f'Skip rate: {skip_rate}')

    # GET SIGNIFICANT FRAMES
    if n_threads == 1:
        sig_frames, reconstruction_map = \
            get_sig_frames_serial(input_file, similarity_threshold, skip_rate)
    else:
        sig_frames, reconstruction_map = \
            get_sig_frames_parallel(input_file, 6, similarity_threshold, skip_rate)

    # OUTPUT FILE
    # Define output video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    # Write significant frames to file
    for frame in sig_frames:
        out.write(frame)
    # Release resources
    out.release()
    cap.release()

    return reconstruction_map


def remap_results_to_original_video(model, compressed_results, reconstruction_map):
    if model == 'clip':
        for frame in compressed_results:
            for interval in frame['intervals']:
                interval[0] = reconstruction_map[interval[0]][0]
                interval[1] = reconstruction_map[interval[1]][1]
    else:
        for frame in compressed_results:
            # Replace "frame_index" with "interval"
            frame['interval'] = reconstruction_map[frame['frame_index']]
            del frame['frame_index']

    return compressed_results


def get_overall_accuracy(response_for_each_model):
    resp = {
        'intervals': [],
        'accuracies': [],
        'num_frames': response_for_each_model['num_frames']
    }
    models = ('clip', 'yolov5', 'efficientnet', 'resnet', 'inceptionv3')
    for i in range(response_for_each_model['num_frames']):
        resp['intervals'].append([i, i+1])
        avg_acc = 0
        num_models_that_answered = 0
        for model_name in models:
            if model_name in response_for_each_model.keys():
                if model_name == 'clip':
                    found = False
                    for match in response_for_each_model[model_name]:
                        if found:
                            break
                        for interval in match['intervals']:
                            if interval[0] <= i <= interval[1]:
                                avg_acc += match['accuracy'] / 100
                                num_models_that_answered += 1
                                found = True
                                break
                else:
                    for match in response_for_each_model[model_name]:
                        if match['interval'][0] <= i <= match['interval'][1]:
                            avg_acc += float(match['accuracy'])
                            if avg_acc > 1:
                                avg_acc /= 100
                            num_models_that_answered += 1
        resp['accuracies'].append(avg_acc / num_models_that_answered)
    return resp


def get_num_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def get_sig_frames_parallel(video_path, num_workers, similarity_threshold, skip_rate):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    significant_frames = []
    reconstruction_map = []

    # Create worker threads
    interval_len = int(total_frames / num_workers)
    workers = []
    for i in range(num_workers):
        # Compute the current worker's interval
        interval = (i * interval_len, (i + 1) * interval_len)
        if i == num_workers - 1:
            interval = (interval[0], total_frames)
        print(f'Interval: {interval} -- {interval[1] - interval[0]}')

        # Run worker
        worker = VideoCaptureThread(i + 1, video_path, interval, similarity_threshold, skip_rate)
        workers.append(worker)
        worker.start()

    # Wait for all threads to finish
    for worker in workers:
        worker.join()

    # Gather results
    for worker in workers:
        significant_frames.extend(worker.significant_frames)
        reconstruction_map.extend(worker.reconstruction_map)

    print('Significant frames:')
    print(len(significant_frames))
    print('Reconstruction map:')
    print(reconstruction_map)

    print(f'Number of frames kept: '
          f'{len(significant_frames)}/{total_frames} ({len(significant_frames) / total_frames * 100:.2f}%)')
    cap.release()  # Release resources
    return significant_frames, reconstruction_map


def get_sig_frames_serial(video_path, similarity_threshold, skip_rate):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    significant_frames, reconstruction_map = \
        _get_sig_frames_in_interval(cap, (0, total_frames), similarity_threshold, skip_rate)

    cap.release()
    return significant_frames, reconstruction_map


'''
    cap: OpenCV cap object
    interval: 2-tuple (inclusive, exclusive)
    similarity_threshold: between 0 and 1
    skip_rate: number of frames to skip after each iteration
'''


def _get_sig_frames_in_interval(cap, interval, similarity_threshold, skip_rate):
    significant_frames = []
    reconstruction_map = []

    frame_index = interval[0]
    curr_model_frame = None
    model_frame_index = frame_index
    while frame_index < interval[1]:
        ret = cap.grab()
        if not ret:  # haven't reached the end yet
            break

        # Optimization: Skip frames
        if frame_index % skip_rate != 0:
            frame_index += 1
            continue

        _, frame = cap.retrieve()  # Decode
        # print(f"Frame number {frame_index}/{total_frames}")

        if curr_model_frame is None:  # First frame
            # Update model frame: first convert frame to grayscale, then flatten
            curr_model_frame = frame.flatten().astype('float')
            significant_frames.append(frame)
        else:  # Compute similarity between this frame and the model frame
            # Convert frame to grayscale and flatten
            processed_frame = frame.flatten().astype('float')

            # Compute cosine similarity between the two frames
            sim = np.dot(curr_model_frame, processed_frame) / (
                        np.linalg.norm(curr_model_frame) * np.linalg.norm(processed_frame))
            # print(f'Similarity is: {sim}')
            if sim < similarity_threshold:
                # Update model frame: first convert frame to grayscale, then flatten
                curr_model_frame = frame.flatten().astype('float')
                significant_frames.append(frame)
                # Add entry to reconstruction map
                reconstruction_map.append((model_frame_index, frame_index - 1))
                model_frame_index = frame_index

        frame_index += 1

    # Special case: add last interval
    reconstruction_map.append((model_frame_index, frame_index - 1))

    return significant_frames, reconstruction_map


class VideoCaptureThread(threading.Thread):
    def __init__(self, thread_id, video_path, video_interval, similarity_threshold, skip_rate):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.video_path = video_path
        self.video_interval = video_interval
        self.similarity_threshold = similarity_threshold
        self.skip_rate = skip_rate

        # Will be created after run()
        self.significant_frames = None
        self.reconstruction_map = None

    def run(self):
        print(f"Thread-{self.thread_id} processing frames...")
        start = time.time()

        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.video_interval[0])

        # Process frames
        self.significant_frames, self.reconstruction_map = \
            _get_sig_frames_in_interval(cap, self.video_interval, self.similarity_threshold, self.skip_rate)

        cap.release()
        print(f"Thread-{self.thread_id} finished processing frames. Time elapsed: {time.time() - start}")



import json
import sys
import time
import os

DEBUG = True

models = ('clip', 'yolov5', 'efficientnet', 'resnet', 'inceptionv3')

def run_test(test):
    start = time.time()
    response = json.loads(send_request(test['query'], test['video_path'], models))
    duration = time.time() - start

    test_passed = True
    for model_name, correct_matches in test['matches'].items():
        model_intervals = get_model_intervals_from_response(model_name, response)
        num_correct_frames, missed_frames = get_num_correct_frames(correct_matches, model_intervals)
        print(f"MODEL '{model_name}': num correct matches {num_correct_frames}/{len(correct_matches)}")
        if num_correct_frames != len(correct_matches):
            test_passed = False
            print(f"MODEL '{model_name}': missed frames {missed_frames}")

        # dbg_print(f'Model intervals: {model_name} - {model_intervals}')
        # dbg_print(f'Correct matches: {correct_matches}')
    print(f'Time elapsed: {duration}')

    if duration > test['time']:
        print(f'Failed time constraints! {duration}/{time["time"]} seconds')
    return test_passed
    # dbg_print(f'Model response was {response}')


def get_model_intervals_from_response(model_name, response):
    intervals = []
    for match in response[model_name]:
        if model_name == 'clip':
            intervals.extend(match['intervals'])
        else:
            intervals.append(match['interval'])
    return intervals


def get_num_correct_frames(frames_to_check, intervals):
    num_in = 0
    missed_frames = []
    for frame in frames_to_check:
        found_interval = False
        for interval in intervals:
            if interval[0] <= frame <= interval[1]:
                num_in += 1
                found_interval = True
                break
        if not found_interval:
            missed_frames.append(frame)
    return num_in, missed_frames


def main():
    # Change working directory to main "models" folder
    os.chdir('..')
    dbg_print(os.getcwd())

    tests_file = sys.argv[1]

    with open(tests_file, 'r') as f:
        tests = json.load(f)

    for i, test in enumerate(tests['tests']):
        print(f'--------------------- Test {i + 1} ({tests["tests"][i]["video_path"]}) ---------------------')
        test_passed = run_test(test)
        if test_passed:
            print('Test passed!')
        else:
            print('Test failed!')


############ UTILS ############

from datetime import datetime
import socket
import struct

MODEL_SERVER_IP = 'localhost'
MODEL_SERVER_PORT = 5000

def dbg_print(s):
    if DEBUG:
        print(f'[DEBUG:{sys._getframe(1).f_lineno}] {s}')


def send_request(query, video_path, models):
    # Define the address and port of the server
    server_address = ('localhost', 5000)
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect(server_address)

    # Create a dictionary to represent the query
    query_dict = {
        'id': datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3], # Unique id for the request
        'query': query,
        'video_path': video_path,
        'models': models
    }

    # Convert the JSON object to a string
    json_string = json.dumps(query_dict)

    # Send the JSON string to the server
    send_message(client_socket, json_string)
    # Get the response
    response = recv_message(client_socket)

    # Close the socket
    client_socket.close()

    print(f'My response was: {response}')
    return response


# FOR SENDING AND RECEIVING ATOMIC MESSAGES

# Constants for message framing
MSG_HEADER_FORMAT = "!I"  # unsigned int, 4 bytes
MSG_HEADER_SIZE = struct.calcsize(MSG_HEADER_FORMAT)


def send_message(sock, message):
    # Prefix the message with a header indicating its size
    header = struct.pack(MSG_HEADER_FORMAT, len(message))
    full_message = header + message.encode()

    # Send the message over the socket
    sock.sendall(full_message)


def recv_message(sock):
    # Read the message header to determine the message size
    header = b""
    while len(header) < MSG_HEADER_SIZE:
        header += sock.recv(MSG_HEADER_SIZE - len(header))
    msg_len = struct.unpack(MSG_HEADER_FORMAT, header)[0]

    # Read the full message
    msg = b""
    while len(msg) < msg_len:
        chunk_size = min(4096, msg_len - len(msg))
        msg += sock.recv(chunk_size)

    return msg.decode()


if __name__ == '__main__':
    main()

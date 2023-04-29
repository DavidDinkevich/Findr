from datetime import datetime
import socket
import struct
import json

MODEL_SERVER_IP = 'localhost'
MODEL_SERVER_PORT = 5000


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
    query = 'giraffe'
    # Change this to an ABSOLUTE PATH on your computer (we don't support relative yet)
    path = 'C:/Users/david/Documents/github repos/Findr/models/resources/giraffe_and_hippo.mp4'
    models  = ['clip', 'yolov5', 'yolov7']
    send_request(query, path, models)
    
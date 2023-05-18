import struct
import socket
import json


# Define the host and port to communicate with the process
HOST = 'localhost'
PORT = 5000
sock = None

# Queue to hold the list of requests waiting to be processed
# Format: (client_socket, query)
requests = []

# Map that maps request id to client socket
client_socket_map = {}


def start_server():
    global sock
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a specific address and port
    server_address = (HOST, PORT)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(10)
    print(f'Model server is up at: {HOST}:{PORT}')


def wait_for_connection():
    # Wait for a connection
    print("Waiting for a connection...")
    connection, client_address = sock.accept()
    try:
        print("Connection from", client_address)

        # Read a query from the socket and convert to json
        query_string = recv_message(connection)
        if sock is None:
            return
        query_dict = json.loads(query_string)
        print(f'Read query: {query_dict}')

        # Add to queue
        requests.append(query_dict)
        client_socket_map[query_dict['id']] = connection
    except Exception as e:
        print(f'{e}')


def get_next_query():
    # If we have requests waiting in the queue
    if requests:
        return requests.pop(0)
    # Wait for connection
    wait_for_connection()
    # Repeat call recursively, now that we have something in the queue
    return get_next_query()


def send_response(response):
    response_id = response['id']
    client_socket = client_socket_map[response_id]
    response = json.dumps(response) # Convert json to string
    send_message(client_socket, response)
    client_socket.close()
    del client_socket_map[response_id]


# UTILITY METHODS FOR SENDING ATOMIC MESSAGES

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

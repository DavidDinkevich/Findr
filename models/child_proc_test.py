import sys
import time


if __name__ == '__main__':
    while True:
        # Read a message from the parent process
        message = sys.stdin.readline().strip()

        # If the message is "STOP", break out of the loop and terminate the process
        if message == "STOP":
            break

        sys.stderr.write(f'Child: got message: {message}\n')
        time.sleep(2)
        # Do some processing on the message (here, just capitalize it)
        response = message.upper()
        sys.stderr.write(f'Child: sending message: {response}\n')

        # Send the response back to the parent process
        sys.stdout.write(response + "\n")
        sys.stdout.flush()

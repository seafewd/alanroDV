import socket
import errno
import sys
from threading import Thread

HEADER_LENGTH = 10
client_socket = None


# Connects to the server
def connect(ip, port, my_username, error_callback):

    global client_socket

    # create a socket
    # AF_INET - address family, IPv4
    # SOCK_STREAM - TCP connection based
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to a given ip and port
        client_socket.connect((ip, port))
    except Exception as e:
        # connection error
        error_callback('Connection error: {}'.format(str(e)))
        return False

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    return True

# sends a message to the server
def send(message):
    # encode message to bytes, prepare header and convert to bytes - then send
    message = message.encode('utf-8')
    message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)


# starts listening function in a thread
# incoming_message_callback - callback to be called when new message arrives
# error_callback - callback to be called on error
def start_listening(incoming_message_callback, error_callback):
    Thread(target=listen, args=(incoming_message_callback, error_callback), daemon=True).start()


# Listens for incoming messages
def listen(incoming_message_callback, error_callback):
    while True:

        try:
            # loop over received messages (might be more than one) and print them
            while True:

                # receive our "header" containing username length, its size is defined and constant
                username_header = client_socket.recv(HEADER_LENGTH)

                # if we didn't receive any data, server gracefully closed a connection, for example using socket.close()
                if not len(username_header):
                    error_callback('Connection closed by the server')

                # convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # now do the same for message
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                # print message
                incoming_message_callback(username, message)

        except Exception as e:
            # any other exception - something happened, exit
            error_callback('Reading error: {}'.format(str(e)))
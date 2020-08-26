import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# socket type
# AF_INET - address family, IPv4
# SOCK_STREAM - TCP connection based
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# socket option level to sort potential port collision when reconnecting
server_socket.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

# bind IP and port
server_socket.bind((IP, PORT))

# config the socket to listen
server_socket.listen()

# list of clients/sockets
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


# handle message receiving
def receive_message(client_socket):
    try:
        # receive our "header" containing message length, its size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        # convert header to int value and strip to exclude spaces
        message_length = int(message_header.decode("utf-8").strip())

        # return an object of message header and message data
        return {
            "header": message_header,
            "data": client_socket.recv(message_length)
        }

    # fatal error!
    except:
        return False


while True:
    print("started")
    read_sockets, _, exception_sockets = select.select(
        # read list - the things we wanna to read in
        sockets_list,
        # sockets that we're gonna write
        [],
        # sockets we might error on
        sockets_list
    )
    for notified_socket in read_sockets:
        # if notified socket is server socket, someone just connected - handle it
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue
            # add client to sockets list
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        # else existing socket is sending a message
        else:
            # receive message
            message = receive_message(notified_socket)
            # message is false - delete socket
            if message is False:
                print("Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # get user by notified socket, so we know who sent the message
            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # iterate over connected clients and broadcast message
            for client_socket in clients:
                # dont send it back to the sender
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] +
                        user['data'] +
                        message['header'] +
                        message['data']
                    )

    # handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

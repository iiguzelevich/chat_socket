import os
import select
import socket
import sys
from dotenv import load_dotenv

load_dotenv()

server_address = (os.getenv('HOST'), int(os.getenv('PORT')))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(float(os.getenv('Timeout')))
client_socket.connect(server_address)

sys.stdout.write(
    'enter your name using the command "-my_name:",\n'
    'enter to exit - "_exit"\n'
)

while True:
    socket_list = [sys.stdin, client_socket]

    read_ready, write_ready, err_ready = select.select(
        socket_list, [], []
    )

    for r in read_ready:
        if r is client_socket:
            data = r.recv(1024)
            data = data.decode('utf-8')

            if not data:
                sys.stdout.write('DISCONNECTED\n')
                sys.exit()

            else:
                sys.stdout.write(data)

        else:
            msg = sys.stdin.readline()
            if '_exit' == msg.strip():
                client_socket.send(msg.encode('utf-8'))
                sys.exit()

            elif '-my_name' == msg.split(':')[0] and msg.split(':')[1]:
                client_socket.send(msg.encode('utf-8'))

            else:
                client_socket.send(msg.encode('utf-8'))

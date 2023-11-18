"""
author - Yuval Hayun
date   - 17/11/23
socket client
"""
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 16240
HEADER_LEN = 2
MAX_PACKET = 1024


def protocol(my_socket):
    response = ''
    message_len = ''
    while response != '!':
        message_len += response
        response = my_socket.recv(1).decode()
    response = ''
    rounds_num = int(int(message_len) / MAX_PACKET)
    if int(int(message_len) % MAX_PACKET) != 0:
        rounds_num += 1
    for i in range(rounds_num):
        response += my_socket.recv(MAX_PACKET).decode()
    print(response)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(('127.0.0.1', SERVER_PORT))
        request = ""
        while request != "EXIT":
            request = input('enter your request here: ')
            if request == 'TIME' or request == 'NAME' or request == 'RAND' or request == 'EXIT' or request == 'DUMP':
                my_socket.send(request.encode())
                protocol(my_socket)
            else:
                print('invalid')
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()

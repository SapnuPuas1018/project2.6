"""
author - Yuval Hayun
date   - 17/11/23
socket server
"""
import time
import socket
import random

IP = '0.0.0.0'
PORT = 16240
QUEUE_LEN = 1
MAX_PACKET = 4
SHORT_SIZE = 2
SERVER_NAME = 'best server ever'


def return_answer(request):
    if request == 'TIME':
        seconds = time.time()
        local_time = time.ctime(seconds)
        dt_string = "Local time: " + local_time
        return dt_string
    elif request == 'NAME':
        return SERVER_NAME
    elif request == 'RAND':
        random_number = random.randint(1, 10)
        return random_number
    elif request == 'EXIT':
        return 'exit'
    elif request == 'DUMP':

        random_number = random.randint(1, 10000)
        print("DUMP request: returning " + str(random_number) + " As")
        return 'A' * random_number


def protocol(response, client_socket):
    response = str(response)
    client_socket.send((str(len(response)) + '!').encode())
    client_socket.send(response.encode())


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(('0.0.0.0', PORT))
        my_socket.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = my_socket.accept()
            response = ''
            try:
                while response != 'exit':
                    request = client_socket.recv(MAX_PACKET).decode()
                    response = return_answer(request)
                    print('server received ' + request)
                    protocol(response, client_socket)
            except socket.error as err:
                print('received socket error on client socket' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()

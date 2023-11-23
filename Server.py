"""
author - Yuval Hayun
date   - 23/11/23
socket server
"""
import time
import socket
import random
import logging

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

IP = '0.0.0.0'
PORT = 16240
QUEUE_LEN = 1
MAX_PACKET = 4
SHORT_SIZE = 2
SERVER_NAME = 'best server ever'


def return_answer(request):
    """
    :param request:
    :type request: str
    :return: dt_string | SERVER_NAME | random_number
    :rtype: str | int
    """
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


def protocol(response, client_socket):
    """
    :param response:
    :type response:
    :param client_socket:
    :return:
    """
    response = str(response)
    client_socket.send((str(len(response)) + '!').encode())
    client_socket.send(response.encode())


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(('0.0.0.0', PORT))
        my_socket.listen(QUEUE_LEN)
        logging.debug('waiting for connection...')
        while True:
            client_socket, client_address = my_socket.accept()
            response = ''
            try:
                while response != 'exit':
                    request = client_socket.recv(MAX_PACKET).decode()
                    logging.debug('server received: ' + request)
                    response = return_answer(request)
                    protocol(response, client_socket)
            except socket.error as err:
                logging.debug('received socket error on client socket' + str(err))
            finally:
                client_socket.close()
                logging.debug('user disconnected')
    except socket.error as err:
        logging.debug('received socket error on server socket' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()

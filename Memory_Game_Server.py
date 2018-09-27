"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

import socket
import pickle

s = None
s_ip = None
connection = None
client_ip = None


def set_info(server_ip, port):
    global s
    global s_ip
    s_ip = (server_ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(s_ip)


def wait_for_connection():
    global connection
    global client_ip
    s.listen(1)
    while True:
        try:
            connection, client_ip = s.accept()
            print('Connected to {}'.format(client_ip))
        except KeyboardInterrupt:
            return
        finally:
            return 'Connected', connection, client_ip


def send_message(message):
    msg = pickle.dumps(message)
    while True:
        try:
            connection.sendall(msg)
            break
        except OSError:
            print('No server to send message to')


def receive():
    while True:
        try:
            data = connection.recv(1024)
        except UnboundLocalError:
            pass
        finally:
            data = pickle.loads(data)
            # data = data.decode('utf-8')
            # print('\nServer received following message: {}'.format(data))
            return data


def close_connection():
    print('\nConnection closed')
    connection.close()


# set_info('127.0.0.1', 5000)
# wait_for_connection()

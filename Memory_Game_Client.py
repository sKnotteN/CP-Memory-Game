"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

import socket
import pickle

s = None
s_ip = None


def set_info(server_ip, port):
    global s
    global s_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ip = (server_ip, port)
    try:
        s.connect(s_ip)
        return 'Connected'
    except ConnectionRefusedError:
        return 'No server found'


# Try to send and receive a message
def send_message(message):
    print('server trying to send message')
    msg = pickle.dumps(message)
    while True:
        try:
            s.sendall(msg)
            print('client sent this message: ', message)
            break
        except OSError:
            break


def receive():
    print('client waiting for data')
    while True:
        try:
            data = s.recv(1024)
        except UnboundLocalError:
            pass
        finally:
            data = pickle.loads(data)
            return data


def close_connection(sock):
    sock.close()


# set_info('127.0.0.1', 5000)
# sleep(1)
# send_message('hey')
# receive()
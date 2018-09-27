"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""


class Network:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.s_msg = ''
        self.r_msg = ''


class Server(Network):
    def __init__(self, server_ip, port):
        super().__init__(server_ip, port)
        self.c_ip = None
        self.connection = None

        self.server = __import__('Memory_Game_Server')

    def look(self):
        self.server.set_info(self.server_ip, self.port)
        connected, self.c_ip, self.connection = self.server.wait_for_connection()
        return connected

    def receive(self):
        while True:
            try:
                self.r_msg = self.server.receive()
                return self.r_msg
            except ConnectionResetError:
                print('Lost connection to client')

    def send(self, msg):
        self.s_msg = msg
        self.server.send_message(self.s_msg)

    def close(self):
        self.server.close_connection()


class Client(Network):

    def __init__(self, server_ip, port):
        super().__init__(server_ip, port)

        self.client = __import__('Memory_Game_Client')

    def look(self):
        return self.client.set_info(self.server_ip, self.port)

    def receive(self):
        while True:
            try:
                self.r_msg = self.client.receive()
                return self.r_msg
            except ConnectionResetError:
                print('Lost connection to host')

    def send(self, msg):
        self.s_msg = msg
        self.client.send_message(self.s_msg)

    def close(self):
        self.client.close_connection()

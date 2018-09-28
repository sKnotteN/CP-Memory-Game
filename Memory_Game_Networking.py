"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""


# Lag ein parent klasse for server og client
class Network:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.s_msg = ''
        self.r_msg = ''


# Arv Network klassa og lag ein klasse for serveren
class Server(Network):
    def __init__(self, server_ip, port):
        # Arv init variablane frå parent
        super().__init__(server_ip, port)

        # Legg til klient ip og connection variabel som skal bli sett seinare
        self.c_ip = None
        self.connection = None

        # Importer Memory_Game_server
        self.server = __import__('Memory_Game_Server')

    # Lagre informasjonen og vent på tilkopling fra klienten, returner så svaret som kjem frå Memory_Game_Server
    def look(self):
        self.server.set_info(self.server_ip, self.port)
        connected, self.c_ip, self.connection = self.server.wait_for_connection()
        return connected

    # Vent på svar fra klienten
    def receive(self):
        while True:
            try:
                self.r_msg = self.server.receive()
                return self.r_msg
            except ConnectionResetError:
                print('Lost connection to client')

    # Send svar til klienten
    def send(self, msg):
        self.s_msg = msg
        self.server.send_message(self.s_msg)

    # Stop tilkoplinga til klienten
    def close(self):
        self.server.close_connection()


# Arv Network klassa og lag ein klasse for klienten
class Client(Network):
    def __init__(self, server_ip, port):
        # Arv init variablane frå parent
        super().__init__(server_ip, port)

        # Importer Memory_Game_Client
        self.client = __import__('Memory_Game_Client')

    # Lagre informasjonen om serveren
    def look(self):
        return self.client.set_info(self.server_ip, self.port)

    # Vent på svar fra serveren
    def receive(self):
        while True:
            try:
                self.r_msg = self.client.receive()
                return self.r_msg
            except ConnectionResetError:
                print('Lost connection to host')

    # Send svar til serveren
    def send(self, msg):
        self.s_msg = msg
        self.client.send_message(self.s_msg)

    # Stop tilkoplinga til serveren
    def close(self):
        self.client.close_connection()

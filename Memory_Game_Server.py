"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# Importer dei offentlige bibloteka
import socket
import pickle

# Set nokre variablar som skal vere lett tilgjengelege
s = None
s_ip = None
connection = None
client_ip = None


# Lagrer informasjonen som skal bli brukt i variabler. Lag ein TCP IPv4 socket
def set_info(port):
    global s
    global s_ip
    ip = socket.gethostbyname(socket.gethostname())
    s_ip = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(s_ip)


# Vent på at ein klient skal kople til på satt ip og port, returner 'Connected' tilkopling og klient ip på tilkopling
def wait_for_connection():
    global connection
    global client_ip
    s.listen(1)
    while True:
        try:
            connection, client_ip = s.accept()
            print('Connected to {}'.format(client_ip))
            return 'Connected', connection, client_ip
        except Exception:
            return 'Interrupted', None, None


# Send ein beskjed til klienten. Bruk pickle til og enkelt sende variablar
def send_message(message):
    msg = pickle.dumps(message)
    while True:
        try:
            connection.sendall(msg)
            break
        except OSError:
            break


# Vent på ein melding frå klienten. Decode meldingen med pickle og returner meldingen
def receive():
    data = None
    while True:
        try:
            data = connection.recv(1024)
        except OSError:
            return None
        finally:
            if data:
                data = pickle.loads(data)
                return data


# Stop tilkoplinga
def close_connection():
    s.close()

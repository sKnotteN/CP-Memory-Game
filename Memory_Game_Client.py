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


# Vent på at ein klient skal kople til på satt ip og port, returner 'Connected' tilkopling og klient ip på tilkopling
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


# Send ein beskjed til serveren. Bruk pickle til og enkelt sende variablar
def send_message(message):
    msg = pickle.dumps(message)
    while True:
        try:
            s.sendall(msg)
            break
        except OSError:
            break


# Vent på ein melding frå server. Decode meldingen med pickle og returner meldingen
def receive():
    while True:
        try:
            data = s.recv(1024)
        except UnboundLocalError:
            pass
        finally:
            data = pickle.loads(data)
            return data


# Stop tilkoplinga
def close_connection(sock):
    sock.close()


# set_info('127.0.0.1', 5000)
# sleep(1)
# send_message('hey')
# receive()
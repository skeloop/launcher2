#Client Skript
import socket
import time
import threading
import version_checker
import keyboard
version_checker.init_path("dev")

HOST = "localhost"
PORT = 6789


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def Disconnect():
    client.close()

def SendToServer(_message):
    client.send(_message.encode())

username = ""

def Handle():
    #SendToServer("request_version_from_server")
    SendToServer("ready_for_login")
    while True:
        data = client.recv(1024)
        message = data.decode()

        if message == "login":
            text = input('Bitte gebe deinen Benutzernamen ein: ')
            username = text
            SendToServer(text)
        elif message == "password":
            text = input('Bitte gebe dein Passwort ein: ')
            SendToServer(text)
        elif message == "login_deny":
            print("Falsches Passwort! Sitzung wurde vom Host beendet.")
        elif message == "login_accept":
            print("Willkommen "+str(username))
            print("Benutze /help um eine Liste an Befehlen zu erhalten")
            t1 = threading.Thread(target=Recieve)
            t1.start()
            Write()


def Recieve():
    print("ready to recieve")
    while True:
        data = client.recv(1024)
        message = data.decode()
        print(">"+str(message))

def Write():
    print("wait for input")
    while True:
        text = input('')
        SendToServer(text)

def get_server_version():
    client.send("request_server_version".encode())
    message = client.recv(1024).decode()
    return message

def update(_version):
    print("Eine neue Version is verfügbar: "+str(_version))
    print("Drücke (1) zum herunterladen oder (2) zum fortfahren...")
    while True:
        if keyboard.is_pressed("1"):
            print("Warte auf Packet...")
            time.sleep(2)
            print("Fertig")
            break
        if keyboard.is_pressed('2'):
            print("Fortfahren...")
            time.sleep(1.5)
            print("Client wird gestartet...")
            break
            
def Version():
    server_version = get_server_version()
    local_version = version_checker.get_local_version()
    print("Lokale version: "+str(local_version))
    print("Server version: "+str(server_version))
    if local_version != server_version:
        update(server_version)

Version()
Handle()










# Server Skript
import socket
from dataclasses import dataclass
import threading
import version_checker

server_version = "2.6"
version_checker.init_path("server")

@dataclass
class UserInfo:
    name: str 
    password: str 
    client: str
    tags: []
        
user_infos = [UserInfo(name="Nick", password="1209", client="", tags="admin"), 
              UserInfo(name="Fanboy", password="1234", client="",tags=""), 
              UserInfo(name="Noel", password="1234", client="",tags="")
              ]
def get_name_ny_client(_client):
    for user in user_infos:
        print(user.client)
        print(_client)
        print("--------------")
        if user.client == _client:
            return user.client


def get_client_by_name(_name):
    for user in user_infos:
        if user.name == _name:
            return user
    return "NULL"

def client_has_tag(_tag, _name):
    client = get_client_by_name(_name)
    if client != "NULL":
        for tag in client.tags:
            if tag == _tag:
                return True
        return False
    return False

clients = []
def UserConnect(client):
    clients.append(client)
def UserDisconnect(client):
    clients.remove(client)

def CheckForUser(_name): 
    for d in user_infos:
        if d.name == _name:
            return True
    return False

def CheckPasswordForUser(_name, _password):
    for d in user_infos:
        if d.name == _name and d.password == _password:
            return True
    return False

def Broadcast(_message):
    print("broadcast: "+str(_message))
    for client in clients:
        message = "[Anonym] "+str(_message)
        client.send(message.encode())

def CheckCommand(_command, _client):
    if _command == "/help":
        _client.send("Befehle:\n/help - Zeigt diese Liste\n/quit - Programm verlassen".encode())
        return True
    if _command == "/quit":
        _client.send("Du hast die Verbindung getrennt.".encode())
        UserDisconnect(_client)
        return True
    if _command == "/profile":
        message = "Name: " +str(get_name_ny_client(_client))
        _client.send(message.encode())
        return True



HOST = "localhost"
PORT = 6789

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("Server wurde gestartet")

# Handle Client Message
def Handle(_client):
    client_status = "hello"
    user_data = UserInfo
    while True:
        try:
            data = _client.recv(1024)
            message = data.decode()
            print("Nachricht von Client: "+str(message))
        except:
            print("Verbindung unterbrochen: "+str(_client))
            break
        if not data:
            print("Data NULL: Server close")
            break
            
        if message == "request_server_version":
            print(server_version)
            _client.send(server_version.encode())
            continue
        if message == "ready_for_login":
            _client.send("login".encode())
            client_status = "login"
            continue
        if client_status == "login":
            user_data.name = message
            _client.send("password".encode())
            client_status = "password"
            continue

        if client_status == "password":
            print(message)
            user_data.password = message
            print(user_data.name)
            print(user_data.password)
            if CheckPasswordForUser(user_data.name, user_data.password):
                _client.send("login_accept".encode())
                print("Ein Benutzer hat sich angemeldet.")
                print("Name: " + str(user_data.name))
                print("Passwort: " + str(user_data.password))
                print("Client: "+ str(_client)) 
                client_status = "online"
                UserConnect(_client)
                user_data.client = _client
                continue
            else:
                _client.send("login_deny".encode())
                print("Ein Benutzer hat versucht sich anzumelden.")
                print('Anfrage abgelehnt. Grund: Falsches Passwort')
                UserDisconnect(_client)
                _client.close()
                break

        if client_status == "online":
            if CheckCommand(message, _client):
                continue
            Broadcast(message)

# Client connection
def Recieve():
    while True:
        client, adress = server.accept()
        print("Client verbindet sich: " + str(adress))

        thread_handle = threading.Thread(target=Handle, args=(client,))
        thread_handle.start()

Recieve()



    







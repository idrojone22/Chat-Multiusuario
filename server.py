import socket
import threading
import json

def client_thread(client_socket, clients, usernames, username):
   
    # usernames[client_socket] = username
    print(f"\n[+] El usuario {username} se ha conectado al chat")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n[+] El usuario {username} ha entrado al chat\n\n".encode())

    while True:
        try: 
            message = client_socket.recv(1024).decode()

            if not message:
                break
            
            if message == "!usuarios":
                client_socket.sendall(f"\n[+] Listado de usuarios conectados: {','.join(usernames.values())}\n\n".encode())
                continue

            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    #del usernames[client_socket]

def server_program(): 
    host = '192.168.1.44'
    port = 12345

    clients = []
    usernames = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"\n[+] El servidor está en escucha de conexiones entrantes...")
    
    while True:
        client_socket, address = server_socket.accept()
        username = client_socket.recv(1024).decode()
        clients.append(client_socket)

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames, username))
        thread.daemon = True
        thread.start()

        print(f"\n[+] Se ha conectado un nuevo cliente: {address}, {usernames}")
    
    server_socket.close()

if __name__ == '__main__':
    server_program()

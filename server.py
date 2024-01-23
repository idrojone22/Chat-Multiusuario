#!/usr/bin/env python3

import socket # Para crear sockets
import threading # Para crear hilos 

def client_thread(client_socket, clients, usernames):

    """
    Esta función se encarga de manejar una sola conexión de cliente.

    Recibe tres argumentos:
    client_socket: socket para el cliente conectado
    clients: lista de todos los sockets con clientes conectados
    usernames: diccionario que mapea los sockets de cliente a sus nombres de usuario
    """

    username = client_socket.recv(1024).decode() # Lee hasta 1024 bytes dek siket y los decodifica como UTF-8
    usernames[client_socket] = username  # Almacena el nombre de usuario asignado al socket del cliente al nombre de usuario
    print(f"\n[+] El usuario {username} se ha conectado al chat") # Imprime el mensaje cada vez que un usuario se conecta 

    """
    Este bucle envia un mensaje a todos los clientes conectados excepto al que ha entrado, informando de
    que un nuevo usuario ha entrado al chat
    """
    for client in clients:

        if client is not client_socket:
            client.sendall(f"\n[+] El usuario {username} ha entrado al chat\n\n".encode())

    while True: # Este bucle se ejecuta continuamente mientras el usuario esta conectado.

        """
        Intenta recibir un mensaje del cliente. 
        Con el metodo recv() vuelve a leer hasta 1024 bytes del socket y los decodifica como UTF-8
        Luego verificamos si el mensaje esta vacio, lo qu eindica que el cliente esta desconectado. 
        En caso de ser asi sale del bucle
        """
        try: 
            message = client_socket.recv(1024).decode()

            if not message:
                break
            
            #Este bucle envia el mensaje recibido a todos los clientes conectados excpeto al cliente actual
            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        
        # Captura cualquier error que pueda ocurrir durante la cominicación con el cliente y sale del bucle
        except:
            break
    
def server_program(): # Programa principal del servidor.

    # Crea un socket, lo asocia a un puerto y comienza a escuchar conexiones entarntes

    host = '192.168.1.44'
    port = 12345

    # Crean un objeto socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TIME_WAIT
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"\n[+] El servidor está en escucha de conexiones entrantes...")

    clients = []
    usernames = {}
    
    """
    Espera una conexión entrante y la acepta. 
    El método accept() devuelve una tupla que contiene el objeto de socket del cliente y la dirección del cliente. 
    El socket del cliente se agrega a la lista clients.
    """
    while True:
        
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\n[+] Se ha conectado un nuevo cliente: {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.daemon = True
        thread.start()
    
    server_socket.close()

if __name__ == '__main__':
    
    server_program()
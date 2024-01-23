#!/usr/bin/env python3

import socket # Para creat un socket y conectarse al servidor
import threading # Para crear hilos para manejar el envío y recepción de mensajes
from tkinter import * # Para crear la interfaz gráfica de usuario
from tkinter.scrolledtext import ScrolledText # Para crear un widget de texto con desplazamiento para mostrar mensajes


"""
Esta función se encarga de enviar mensajes al servidor. Recibe cuatro argumentos:

client_socket: El objeto de socket del cliente
username: El nombre de usuario del cliente
text_widget: El widget de texto donde se mostrarán los mensajes
entry_widget: El widget de entrada donde se escribe el mensaje que se enviará

La función comienza recuperando el mensaje del widget de entrada. 
Luego, formatea el mensaje con el nombre del usuario, concatenando ambos con un símbolo de mayor que ">". 
A continuación, codifica el mensaje en UTF-8 y lo envía al servidor utilizando el objeto de socket del cliente.

Una vez que el mensaje se envía, la función borra el widget de entrada para que el usuario pueda escribir un nuevo mensaje. 
Luego, inserta el mensaje enviado en el historial de chat, que se muestra en el widget de texto. 
Por último, deshabilita el widget de texto para que el usuario no pueda modificarlo hasta que haya enviado un nuevo mensaje.
"""
def send_message(client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disable')

"""
Esta función se encarga de recibir mensajes del servidor. Recibe dos argumentos:

client_socket: El objeto de socket del cliente
text_widget: El widget de texto donde se mostrarán los mensajes

La función comienza creando un bucle infinito que se ejecutará continuamente para recibir mensajes del servidor. 
Dentro del bucle, la función intenta recibir un mensaje del servidor, leyendo hasta 1024 bytes a la vez.

Si el mensaje recibido no está vacío, la función lo formatea con el nombre del usuario, concatenando ambos con un símbolo de mayor que ">". 
A continuación, inserta el mensaje recibido en el historial de chat, que se muestra en el widget de texto. 
Por último, deshabilita el widget de texto para que el usuario no pueda modificarlo hasta que haya recibido un nuevo mensaje.
"""
def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disable')

        except:
            break

"""
Esta función es el programa principal del cliente. 
Se encarga de crear la conexión con el servidor, configurar la interfaz gráfica de usuario y manejar el envío y recepción de mensajes.

La función comienza definiendo la dirección del host (localhost) y el número de puerto (12345) para el servidor. 
A continuación, crea un objeto de socket, lo conecta a la dirección y puerto del servidor especificados y establece una conexión con el servidor.

Luego, la función solicita al usuario que ingrese su nombre de usuario, lo codifica en UTF-8 y lo envía al servidor.

A continuación, la función crea una nueva ventana de Tkinter y le da el título "Chat". 
Luego, crea un widget de texto con desplazamiento para mostrar los mensajes. 
El widget de texto se deshabilita inicialmente para que el usuario no pueda modificarlo hasta que haya enviado un mensaje.

Finalmente, la función crea un botón para enviar mensajes.
 El botón está vinculado a la función send_message(), que se encargará de enviar el mensaje al servidor.
"""
def client_program():
    host = '192.168.1.44'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input(f"\n[+] Introduce tu usuario: ")
    client_socket.sendall(username.encode())

    window = Tk()
    window.title("Chat")

    # ScrolledText widget
    text_widget = ScrolledText(window, state='disable')
    text_widget.pack(padx=5, pady=5)

    # Button send 
    frame_widget = Frame(window)
    frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)
    
    button_widget = Button(frame_widget, text="Enviar")
    button_widget.pack(side=RIGHT, padx=5)

    # Entry widget
    entry_widget = Entry(frame_widget)
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=BOTH, expand=1)

    # Start a thread for receiving messages
    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()

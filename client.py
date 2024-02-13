import socket
import json
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message(client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disable')

def receive_message(client_socket, text_widget, username, window_closed):
    while not window_closed:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disable')

        except:
            break

def list_users_request(client_socket):
    client_socket.sendall("!usuarios".encode())

def exit_request(client_socket, username, window, window_closed):
    window_closed = True
    client_socket.sendall(f"\n[!] El usuario {username} ha abandonado el chat.\n\n".encode())
    client_socket.close()
    window.quit()

def client_program():
    host = '192.168.1.44'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    username = input("Introduzca su nombre de usuario: ")
    client_socket.sendall(username.encode())

    window = Tk()
    window.title("Chat")
    window_closed = False  # Variable de bandera para indicar si la ventana ha sido cerrada

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)

    frame_widget = Frame(window)
    frame_widget.pack(padx=5, pady=2, fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget, font=("Arial", 14))
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=X, expand=1)

    button_widget = Button(frame_widget, text='Enviar', command=lambda: send_message(client_socket, username, text_widget, entry_widget))
    button_widget.pack(side=RIGHT, padx=5)

    # users_widget = Button(window, text="Listar usuarios", command=lambda: list_users_request(client_socket))
    # users_widget.pack(padx=5, pady=5)

    exit_widget = Button(window, text="Salir", command=lambda: exit_request(client_socket, username, window, window_closed))
    exit_widget.pack(padx=5, pady=5)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget, username, window_closed))
    thread.daemon = True
    thread.start()

    window.mainloop()
    window_closed = True  # Marcar que la ventana se ha cerrado
    client_socket.close()

if __name__ == '__main__':
    client_program()


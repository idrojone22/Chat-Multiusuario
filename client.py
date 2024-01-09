#!/usr/bin/env python3
"""
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_massage(client_socket, username, text_widget, entry_widget):
    
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n")
    text_widget.configure(state='disable')

def recive_messege(client_socket, text_widget):

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
            
def client_program():

    host = '192.168.1.44'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input(f"\n[+] Introduce tu usuario: ")
    client_socket.sendall(username.encode())


    window = Tk()
    window.title("Chat")

    text_widget = ScrolledText(window, state='disable')
    text_widget.pack(padx=5, pady=5)

    entry_widget = Entry(window)
    entry_widget.bind("<Return>", lambda _: send_massage(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(pady=5, padx=5, fill=BOTH, expand=1)

    thread = threading.Thread(target=recive_messege, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()


if __name__ == '__main__':
    client_program()
"""

import socket
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
    text_widget = ScrolledText(window, state='disable', height=15, width=50, wrap=WORD)
    text_widget.pack(padx=10, pady=10)

    # Entry widget
    entry_widget = Entry(window, width=50)
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Start a thread for receiving messages
    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()

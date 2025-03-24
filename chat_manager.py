import socket
import os

from cipher import AESCipher
from threading import Thread

from message import Message

server_addr = ('127.0.0.1', 15000)


class ChatManager:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def register(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(server_addr)

        conn.send(f'Registration {self.username} {self.password}'.encode())
        self.conn = conn
        print(self.read())
        conn.close()

    def extract_session_key(self, data):
        cipher = AESCipher(self.password.encode())
        session_key = cipher.decrypt(data)
        return session_key

    def login(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(server_addr)
        # cipher = AESCipher()
        conn.send(f'Login {self.username}'.encode())

        self.conn = conn

        data = conn.recv(2048).decode()
        protected_session_key = bytearray.fromhex(data.split(' ')[1])
        session_key = self.extract_session_key(protected_session_key)
        self.cipher = AESCipher(session_key)

        self.sendp(f'Hello {self.username}')

        data = self.read()
        print(data.decode())

    def decrypt_message(self, data):
        return self.cipher.decrypt(data)

    def encrypt_message(self, data):
        return self.cipher.encrypt(data)

    def read(self):
        data = b''
        while packet := self.conn.recv(2048):
            data += packet
            if len(packet) < 2048:
                break

        return data

    def readp(self):
        data = self.decrypt_message(self.read())
        print('received:', data)
        return data

    def read_message(self):
        data = self.readp()
        return Message.from_data(data)

    def sendp(self, data):
        if isinstance(data, str):
            data = data.encode()

        print("sending:", data)
        encrypted_data = self.encrypt_message(data)
        self.send(encrypted_data)

    def send(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')

        print(len(message))
        for i in range(0, len(message), 2048):
            self.conn.send(message[i:i+2048])

    def read_and_print_messages(self):
        while True:
            data = self.readp()
            print('New message:', data, flush=True)

    def read_messages(self):
        self.thread = Thread(target=self.read_and_print_messages)
        self.thread.start()

    def send_public_file(self, path: str):
        with open(path, 'rb') as f:
            data = f.read()
            filename = os.path.basename(path)
            data = f"Public file, filename={filename}, length={len(data)}\n\r".encode() + data
            return self.sendp(data)

    def send_public_message(self, message):
        data = f"Public message, length={len(message)}\n\r{message}"
        return self.sendp(data)

    def send_private_message(self, receivers, message):
        if isinstance(receivers, list):
            receivers = ','.join(receivers)

        data = f"Private message, length={len(message)} to {receivers}\n\r{message}"
        return self.sendp(data)

    def send_bye_signal(self):
        self.sendp('Bye.')

    def list_attendees(self):
        return self.sendp("Please send the list of attendees.")


def main():
    username = input("enter username: ")
    password = input("enter password: ")
    cm = ChatManager(username, password)
    cm.register()
    cm.login()
    cm.read_messages()
    while data := input():
        if data.startswith('bb '):
            cm.send_public_message(data[3:])
        elif data.startswith('pp '):
            cm.send_private_message(data[3:data.find('|')], data[data.find('|') + 1:])
        else:
            cm.sendp(data)


if __name__ == '__main__':
    main()

import socket
import threading
import glob
import os
import protocol27
import random
import shutil
import subprocess
import pyautogui
import io



max_connections = 20
HOST = '0.0.0.0'
PORT = 8822
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
clients = []

print("Server is up and running")

def Waitforconnections():
    while True:
        print("wait for connections")
        client_socket, client_address = server_socket.accept()
        print("Client connected")
        threading.Thread(target=handle_client(client_socket,client_address),args=(client_socket,client_address)).start()

def handle_client(client_socket,client_address):
    clients.append(client_socket)
    print("Client connected")
    while True:
        isvalid,data = protocol27.get_msg(client_socket)
        if (isvalid == False): break
        if protocol27.check_cmd(data) == True:
            if str(data).startswith("DIR"):
                folder_path = data[4:]
                files_list = os.listdir(folder_path)
                data = protocol27.create_msg(str(files_list))
                client_socket.send(data.encode())

            if str(data).startswith("DELETE"):
                folder_path = data[7:]
                os.remove(folder_path)
                print("the data has been removed! ")

            if str(data).startswith("COPY"):
                parts = data.split(' ')
                source_path = str(parts[1])
                dest_path = str(parts[2])
                shutil.copy(source_path, dest_path)
                print("the data has been copied! ")

            if str(data).startswith("EXECUTE"):
                app = data[8:]
                os.startfile(app)
                print("the app has launched")

            if str(data) == "TAKE_SCREENSHOT":
                image = pyautogui.screenshot()
                image.save(r'C:\pythonProject\image.png')
                print("the screenshot has been saved")

            if str(data).startswith("SEND_PHOTO"):
                destination = data[11:]
                print(destination)
                image = pyautogui.screenshot()
                image.save(destination)

            if data.upper() == "EXIT":
                client_socket.close()
                server_socket.close()

if __name__ == "__main__":
    server_socket.listen(max_connections)
    print("server is listening")
    Accept_Thread = threading.Thread(target= Waitforconnections()).start()
    Accept_Thread.join()
    server_socket.close()

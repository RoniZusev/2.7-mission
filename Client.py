import socket
import protocol27

PORT = 8822
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((("127.0.0.1", PORT)))
print(f"Connected to server at 127.0.0.1 :{PORT}")

while True:
    message = input("Enter message (type 'exit' to quit): ")
    if message.lower() == 'exit':
       print("Closing connection.")
       break

    data = protocol27.create_msg(message)
    client_socket.send(data.encode())
    isvalid,response = protocol27.get_msg(client_socket)
    print(f"Server replied: {response}")

client_socket.close()
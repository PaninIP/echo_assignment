import socket
import time


#инициализация сокета сервера
HOST = "127.0.0.1"
PORT = 9876
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#сервер слушает входящие соединения
server_socket.listen()
print(f"Server started on address {HOST}:{PORT}")

#принятие клиента
connection, address = server_socket.accept()
print(f"Client connected: {address}")

#расшифровка сообщения от клиента
while True:
    data = connection.recv(1024)

    if not data:
        break

    timestamp = time.time() #время на момент выполнения команды
    message = data.decode("utf-8").rstrip("\n")
    print(message)

    #формирование и отправка ответа клиенту
    response = f"ECHO: {message} [t={timestamp:.6f}]\n"
    connection.sendall(response.encode("utf-8"))

connection.close()
print("Client disconected")
server_socket.close()
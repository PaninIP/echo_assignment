import socket
import time
import threading


#инициализация сокета сервера
HOST = "127.0.0.1"
PORT = 9876
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#сервер слушает входящие соединения
server_socket.listen()
print(f"Server started on address {HOST}:{PORT}")

def handle_client(connection, address):
    print(f"Client connected: {address}")
#расшифровка сообщения от клиента
    try:
        while True:
            data = connection.recv(1024)

            if not data:
                break

            timestamp = time.time() #время на момент выполнения команды
            message = data.decode("utf-8").rstrip("\n")
            print(f"{address} {message}")

            #формирование и отправка ответа клиенту
            response = f"ECHO: {message} [t={timestamp:.6f}]\n"
            connection.sendall(response.encode("utf-8"))
    except OSError as error:
        print(f"Connection error {address}: {error}")
    finally:
        connection.close()
        print(f"Client disconected {address}")

#принятие клиента
try:
    while True:
        connection, address = server_socket.accept()
        #print(f"Client connected: {address}")
        #handle_client(connection, address)
        
        thread = threading.Thread(
            target=handle_client,
            args=(connection, address)
        )

        thread.start()
except KeyboardInterrupt:
    print("\nServer stopped by user!!!")
finally:
    server_socket.close()
    print("Server socket closed :(")
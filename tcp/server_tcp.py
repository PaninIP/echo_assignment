import socket
import time
import threading
import signal


#инициализация сокета сервера
HOST = "127.0.0.1"
PORT = 9876
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

#сервер слушает входящие соединения
server_socket.listen()
server_socket.settimeout(1.0)
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
        print(f"Client disconnected {address}")

stop_event = threading.Event()

def shutdown_handler(signum, frame):
    print("\nShutdown requested")
    stop_event.set()

# Создание обработчика сигнала, чтобы после нажатия ctrl + C сервер завершал работу
signal.signal(signal.SIGINT, shutdown_handler)

#принятие клиента
try:
    while not stop_event.is_set():
        try:
            connection, address = server_socket.accept()
        except socket.timeout:
            continue
        
        thread = threading.Thread(
            target=handle_client,
            args=(connection, address)
        )

        thread.start()
finally:
    server_socket.close()
    print("Server socket closed :(")
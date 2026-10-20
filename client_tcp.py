import socket
import time
import math

#инициализация сокета клиента
HOST = "127.0.0.1"
PORT = 9877
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (HOST, PORT) #создаём tuple тип, чтобы сувать в функцию без (()), так некрасиво

#подключение к серверу
client_socket.connect(address)
print("Connected to server")

length = 0

while length <= 0 or length > 1000:
    print("Введите кол-во сообщений к отправке (от 1 до 1000): ")
    length = int(input())
    if length == 0:
        print("Введите что-то кроме нуля :)\n")
    elif length > 1000:
        print("Больше тысячи нам не нужно :)\n")
    elif length < 0:
        print("Не сможем мы отправить отрицательное кол-во сообщений :(\n")

rtt_values = []

show_messages = True

total_start = time.perf_counter()
#отправка сообщения серверу
for i in range(length):
    message = f"Hello!!! {i}\n"
    start_time = time.perf_counter() #время отправки сообщения серверу
    client_socket.sendall(message.encode("utf-8"))

    #ответ от сервера
    response = client_socket.recv(1024)
    end_time = time.perf_counter() #время получения ответа от сервера

    #считаем RTT
    rtt = (end_time - start_time)
    rtt_ms = rtt * 1000

    rtt_values.append(rtt_ms)

    #декодировка ответа
    response_message = response.decode("utf-8").rstrip("\n")
    if show_messages:
        print(f"Response from server: {response_message}")
        print(f"RTT: {rtt_ms:.3f} ms")


total_end = time.perf_counter()
total_time = (total_end - total_start)
total_time_ms = total_time * 1000


client_socket.close() #корректно закрываем подключение клиента вот так вот

avg_rtt = sum(rtt_values) / len(rtt_values) #средний rtt за все сообщения
min_rtt = min(rtt_values)
max_rtt = max(rtt_values)

rtt_sorted = sorted(rtt_values)
index_95_percentil = math.ceil(0.95 * len(rtt_values)) - 1
rtt_95_percentil = rtt_sorted[index_95_percentil]
throughput = length / total_time

print()
print("Статистика:")
print(f"Кол-во отправленных сообщений: {length}")
print(f"Пропускная способность (сообщений в секунду) {throughput:.3f}")
print(f"Время отправки всех сообщений: {total_time_ms:.3f} ms")
print(f"Средний RTT: {avg_rtt:.3f} ms")
print(f"Минимальный RTT: {min_rtt:.3f} ms")
print(f"Максимальный RTT: {max_rtt:.3f} ms")
print(f"95-ый процентиль: {rtt_95_percentil:.3f} ms")
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 9876
address = (HOST, PORT)

cnt_clients = 0


print(f"Введи кол-во клиентов для сервера: ")
while cnt_clients <= 0 or cnt_clients > 100:
    cnt_clients = int(input())
    if cnt_clients == 0:
        print(f"\nТы не можешь задать 0 клиентов!!!")
    elif cnt_clients > 100:
        print(f"\nЯ думаю сервер выдержит, но {cnt_clients} клиентов слишком много, в задании нужно 100, давай не будем превышать")
    elif cnt_clients < 0:
        print(f"\nКаким образом ты вообще пытаешься указать отрицательное кол-во клиентов?")

barrier = threading.Barrier(cnt_clients)

def workers(cnt_clients):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(address)

        barrier.wait(timeout=10)

        message = f"Hello {cnt_clients} number! :)\n"
        client.sendall(message.encode('utf-8'))

        response = client.recv(1024)
        print(f"Client {cnt_clients}: {response.decode('utf-8').strip()}")

        time.sleep(2) #для одновременного подключеня многих клиентов

threads = []

for i in range(cnt_clients):
    thread = threading.Thread(
        target=workers,
        args=(i,)
    )

    threads.append(thread)

    thread.start()

for thread in threads:
    thread.join()
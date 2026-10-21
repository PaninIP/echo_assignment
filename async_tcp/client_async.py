import asyncio

HOST = '127.0.0.1'
PORT = 9877
cnt_clients = 0

while cnt_clients <= 0 or cnt_clients > 500:
    print("Введите кол-во клиентов, которые будут подключаться к серверу (от 1 до 500): ")
    try:
        cnt_clients = int(input())
    except ValueError as error:
        print(f"При вводе произошла ошибка:\n{error}")
        continue

    if cnt_clients == 0:
        print("Кол-во клиентов не может быть 0")
    elif cnt_clients > 500:
        print("Для задания больше 500 не надо")
    elif cnt_clients < 0:
        print("Кол-во клиентов не может быть отрицательным")

barrier = asyncio.Barrier(cnt_clients)

async def worker(number):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    try:
        await asyncio.wait_for(await barrier.wait(), timeout=30)

        message = f"Hello {number}\n"

        writer.write(message.encode("utf-8"))
        await writer.drain()

        response = await reader.readline()

        response_message = response.decode("utf-8").rstrip("\n")
        print(response_message)

    finally:
        writer.close()
        await writer.wait_closed()

async def main():

    tasks = []

    for i in range(cnt_clients):
        tasks.append(worker(i))

    await asyncio.gather(*tasks)

asyncio.run(main())
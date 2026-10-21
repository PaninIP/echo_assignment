import asyncio
import grpc

import echo_pb2
import echo_pb2_grpc

HOST = "127.0.0.1"
PORT = 9878

print(f"")
cnt_messages = 0

while cnt_messages <= 0 or cnt_messages > 1000:
    print("Введите кол-во сообщений к отправке (от 1 до 1000): ")
    try:
        cnt_messages = int(input())
    except ValueError as error:
        print(f"При вводе произошла ошибка: {error}")
        continue

    if cnt_messages == 0:
        print("Введите что-то кроме нуля :)\n")
    elif cnt_messages > 1000:
        print("Больше тысячи нам не нужно :)\n")
    elif cnt_messages < 0:
        print("Не сможем мы отправить отрицательное кол-во сообщений :(\n")

async def main():

    async with grpc.aio.insecure_channel(
        f"{HOST}:{PORT}"
    ) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)

        responses = stub.Echo(generate_requests())

        recieved = 0

        async for response in responses:
            print(response.message)
            recieved += 1

        print(f"\nПолучено ответов: {recieved}/{cnt_messages}")


async def generate_requests():
    for i in range(cnt_messages):
        message = f"Hello {i}"

        yield echo_pb2.EchoRequest(message=message)

if __name__ == "__main__":
    asyncio.run(main())
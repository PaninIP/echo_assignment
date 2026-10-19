import asyncio
import time

HOST = "127.0.0.1"
PORT = 9877

async def handle_client(reader, writer):
    pass

async def main():
    server = await asyncio.start_server(
        handle_client,
        HOST,
        PORT
    )

    print(f"Async server started on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

asyncio.run(main())
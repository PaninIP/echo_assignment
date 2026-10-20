import asyncio
import time

HOST = "127.0.0.1"
PORT = 9877

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    print(f"Client connected {address}")
    
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode("utf-8").rstrip("\n")

            print(f"\nClient {address} message: {message}")

            timestamp = time.time()
            response = f"ECHO: {message} [t={timestamp:.6f}]\n"

            writer.write(response.encode("utf-8"))
            await writer.drain()
    except OSError as error:
        print(f"Connection error{address}: {error}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Client disconnected {address}")

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
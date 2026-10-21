import asyncio
import time
import grpc

import echo_pb2
import echo_pb2_grpc

HOST = "127.0.0.1"
PORT = 9878



class EchoServicer(echo_pb2_grpc.EchoServiceServicer):
    async def Echo(self, request_iterator, context):
        received = 0
        async for request in request_iterator:
            received += 1

            if received % 100 == 0:
                print(f"Server received {received} messages")

            timestamp = time.time()
            response = f"ECHO: {request.message} [t={timestamp:.6f}]"

            yield echo_pb2.EchoResponse(message=response)


async def main():

    server = grpc.aio.server()

    echo_pb2_grpc.add_EchoServiceServicer_to_server(
        EchoServicer(),
        server
    )
    
    server.add_insecure_port(f"{HOST}:{PORT}")

    await server.start()
    print(f"gRPC server started on {HOST}:{PORT}")

    try:
        await server.wait_for_termination()
    finally:
        await server.stop(grace=5)
        print("gRPC server stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server was closed")
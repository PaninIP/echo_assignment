"""Простое сравнение RTT и throughput: TCP / asyncio / gRPC.
Перед запуском открой три терминала и запусти серверы отдельно.
"""
import asyncio
import csv
import math
import socket
import time
from pathlib import Path
import sys

import grpc
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).parent / "grpc_echo"))
import echo_pb2
import echo_pb2_grpc

HOST = "127.0.0.1"
COUNTS = [10, 100, 1000]
OUT = Path("graphs")


def tcp(count):
    times = []
    with socket.create_connection((HOST, 9876)) as connection:
        with connection.makefile("rb") as reader:
            total_start = time.perf_counter()
            for i in range(count):
                start = time.perf_counter()
                connection.sendall(f"Hello {i}\n".encode())
                response = reader.readline().decode()
                assert response.startswith(f"ECHO: Hello {i} ")
                times.append((time.perf_counter() - start) * 1000)
            total = time.perf_counter() - total_start
    return times, total


async def async_tcp(count):
    times = []
    reader, writer = await asyncio.open_connection(HOST, 9877)
    try:
        total_start = time.perf_counter()
        for i in range(count):
            start = time.perf_counter()
            writer.write(f"Hello {i}\n".encode())
            await writer.drain()
            response = (await reader.readline()).decode()
            assert response.startswith(f"ECHO: Hello {i} ")
            times.append((time.perf_counter() - start) * 1000)
        total = time.perf_counter() - total_start
    finally:
        writer.close()
        await writer.wait_closed()
    return times, total


async def grpc_stream(count):
    times = []
    async with grpc.aio.insecure_channel(f"{HOST}:9878") as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        stream = stub.Echo()
        total_start = time.perf_counter()
        for i in range(count):
            start = time.perf_counter()
            await stream.write(echo_pb2.EchoRequest(message=f"Hello {i}"))
            response = await stream.read()
            assert response.message.startswith(f"ECHO: Hello {i}")
            times.append((time.perf_counter() - start) * 1000)
        await stream.done_writing()
        total = time.perf_counter() - total_start
    return times, total


def draw(rows, field, filename, title, ylabel):
    plt.figure(figsize=(8, 5))
    for name in ("TCP", "asyncio", "gRPC"):
        results = [row for row in rows if row["server"] == name]
        plt.plot([r["messages"] for r in results],
                 [r[field] for r in results], marker="o", label=name)
    plt.title(title)
    plt.xlabel("Количество сообщений")
    plt.ylabel(ylabel)
    plt.xticks(COUNTS)
    plt.xscale("log")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / filename)
    plt.close()


async def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    tests = [("TCP", tcp), ("asyncio", async_tcp), ("gRPC", grpc_stream)]

    for name, test in tests:
        for count in COUNTS:
            if name == "TCP":
                times, total = test(count)
            else:
                times, total = await test(count)
            sorted_times = sorted(times)
            row = {
                "server": name, "messages": count,
                "avg_rtt_ms": round(sum(times) / count, 3),
                "min_rtt_ms": round(min(times), 3),
                "max_rtt_ms": round(max(times), 3),
                "p95_rtt_ms": round(sorted_times[math.ceil(.95 * count) - 1], 3),
                "throughput": round(count / total, 1),
            }
            rows.append(row)
            print(row)

    with (OUT / "results.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    draw(rows, "avg_rtt_ms", "rtt.png", "Средний RTT", "Миллисекунды")
    draw(rows, "throughput", "throughput.png", "Пропускная способность", "Сообщений в секунду")
    print("Готово: graphs/results.csv, graphs/rtt.png, graphs/throughput.png")


if __name__ == "__main__":
    asyncio.run(main())

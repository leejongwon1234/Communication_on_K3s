# client.py
import grpc
import pingpong_pb2
import pingpong_pb2_grpc
import time
import os

PAYLOAD_SIZE_KB = 1  # 실험할 payload 크기(KB)
ROUNDS = 1000

def measure_rtt(stub, rounds=ROUNDS):
    total_ns = 0
    payload = b'A' * (PAYLOAD_SIZE_KB * 1024)  # 바이트 단위로 구성

    for i in range(rounds):
        start = time.perf_counter_ns()
        response = stub.Ping(pingpong_pb2.PingRequest(sequence=i, payload=payload))
        end = time.perf_counter_ns()
        rtt = end - start

        if i == 0:
            print(f"Initial round delay: {rtt} ns")
        else:
            print(f"Round {i+1} delay: {rtt} ns")
            total_ns += rtt

    print(f"\nAverage delay for payload={PAYLOAD_SIZE_KB} KB: {total_ns / (rounds - 1) / 1000:.2f} µs")

def run():
    server_ip = os.environ.get("SERVER_IP")
    if not server_ip:
        raise ValueError("SERVER_IP 환경변수가 설정되지 않았습니다.")

    with grpc.insecure_channel(f"{server_ip}:50051") as channel:
        stub = pingpong_pb2_grpc.PingPongServiceStub(channel)
        measure_rtt(stub)

if __name__ == '__main__':
    run()

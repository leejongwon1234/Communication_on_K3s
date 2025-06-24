# server.py
import grpc
from concurrent import futures
import pingpong_pb2
import pingpong_pb2_grpc

class PingPongServicer(pingpong_pb2_grpc.PingPongServiceServicer):
    def Ping(self, request, context):
        return pingpong_pb2.PingReply(sequence=request.sequence, payload=request.payload)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    pingpong_pb2_grpc.add_PingPongServiceServicer_to_server(PingPongServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


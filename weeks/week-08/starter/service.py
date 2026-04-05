import time
from concurrent import futures

import grpc

import service_pb2
import service_pb2_grpc


class ServiceImplementation(service_pb2_grpc.SessionsServiceServicer):
    def GetSession(self, request, context):
        return service_pb2.GetSessionResponse(
            id=request.id,
            result=f"Session with id={request.id} was received"
        )

    def SubscribeSessions(self, request, context):
        for i in range(5):
            yield service_pb2.SessionUpdate(
                id=str(i + 1),
                ip=f"192.168.0.{i + 1}",
                status=f"update {i + 1} for client {request.client_id}"
            )
            time.sleep(0.2)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_SessionsServiceServicer_to_server(
        ServiceImplementation(),
        server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server is running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

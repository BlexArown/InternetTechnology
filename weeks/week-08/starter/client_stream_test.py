import grpc
import service_pb2
import service_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.SessionsServiceStub(channel)

        responses = stub.SubscribeSessions(
            service_pb2.SubscribeSessionsRequest(client_id="student-1")
        )

        for item in responses:
            print("id:", item.id, "| ip:", item.ip, "| status:", item.status)


if __name__ == "__main__":
    run()

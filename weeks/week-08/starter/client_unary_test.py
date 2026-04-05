import grpc
import service_pb2
import service_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.SessionsServiceStub(channel)

        response = stub.GetSession(
            service_pb2.GetSessionRequest(id="123")
        )

        print("id:", response.id)
        print("result:", response.result)


if __name__ == "__main__":
    run()

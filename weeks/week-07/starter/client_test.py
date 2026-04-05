import grpc
import service_pb2
import service_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.BookingsServiceStub(channel)

    response = stub.GetBooking(
        service_pb2.GetBookingRequest(id="123")
    )

    print("id:", response.id)
    print("result:", response.result)


if __name__ == '__main__':
    run()

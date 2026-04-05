import grpc
from concurrent import futures

import service_pb2
import service_pb2_grpc


class ServiceImplementation(service_pb2_grpc.BookingsServiceServicer):
    def GetBooking(self, request, context):
        return service_pb2.GetBookingResponse(
            id=request.id,
            result=f"Booking with id={request.id} was received"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_BookingsServiceServicer_to_server(
        ServiceImplementation(),
        server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

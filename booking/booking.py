import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        """Initialize the BookingService and load bookings from a JSON file."""
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetJson(self, request, context) -> booking_pb2.BookingList:
        """Retrieve all bookings in JSON format."""
        all_bookings = []

        for booking in self.db:
            for date_info in booking['dates']:
                user_booking = booking_pb2._Booking(
                    date=date_info['date'],
                    movies_id=booking_pb2.MovieList(movies_id=date_info['movies'])
                )
                all_bookings.append(user_booking)

        return booking_pb2.BookingList(bookings=all_bookings)

    def GetBookings(self, request, context) -> booking_pb2.BookingList:
        """Retrieve bookings for a specific user."""
        user_bookings = []

        for booking in self.db:
            if booking['userid'] == request.id:  # Check if booking belongs to the user
                for date_info in booking['dates']:
                    user_booking = booking_pb2._Booking(
                        date=date_info['date'],
                        movies_id=booking_pb2.MovieList(movies_id=date_info['movies'])
                    )
                    user_bookings.append(user_booking)

        return booking_pb2.BookingList(bookings=user_bookings)

    def AddBooking(self, request, context) -> booking_pb2.Empty:
        """Add a new booking to the database."""
        new_booking = {
            'dates': [
                {
                    'date': request.date,
                    'movies': request.movies_id.movies_id  
                }
            ]
        }

        self.db.append(new_booking) 
        return booking_pb2.Empty()   

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3005')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

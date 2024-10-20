import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetJson(self, request, context):
        all_bookings = []

        for booking in self.db:
            for date_info in booking['dates']:
                user_booking = booking_pb2._Booking(
                    date=date_info['date'],  
                    movies_id=booking_pb2.MovieList(movies_id=date_info['movies'])  
                )
                all_bookings.append(user_booking)

        return booking_pb2.BookingList(bookings=all_bookings)


        return booking_pb2.BookingList(bookings=all_bookings)

    """
    def GetBookings(self, request, context):
        L = []        
        for booking in self.db:
            if booking['userid'] == request.id:
                print("Bookings found!")
                M = booking['dates']
                for b in M:
                    movies = booking_pb2.MovieList(movies_id = b["movies"])
                    L.append(booking_pb2._Booking(date=b['date'], movies_id=movies))
        print('LLLL = ', L)
        bookings = booking_pb2.BookingList(bookings= L)
        print('Bookings: ', bookings)
        return L
    """
    def GetBookings(self, request, context):
        user_bookings = []

        for booking in self.db:
            if booking['userid'] == request.id:  
                for date_info in booking['dates']:
                    user_booking = booking_pb2._Booking(
                        date=date_info['date'],  # Ajouter la date
                        movies_id=booking_pb2.MovieList(movies_id=date_info['movies']) 
                    )
                    user_bookings.append(user_booking)

        return booking_pb2.BookingList(bookings=user_bookings)



    def AddBooking(self, request, context):
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

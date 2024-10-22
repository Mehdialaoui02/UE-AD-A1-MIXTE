import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def save_db(self):
        for booking in self.db:
            for date_info in booking['dates']:
                if isinstance(date_info['movies'], booking_pb2.MovieList):
                    date_info['movies'] = list(date_info['movies'].movies_id)
        
        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump({"bookings": self.db}, jsf, indent=4)
    
    def GetJson(self, request, context) -> booking_pb2.BookingList:
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
        user_bookings = []

        for booking in self.db:
            if booking['userid'] == request.id:  
                for date_info in booking['dates']:
                    user_booking = booking_pb2._Booking(
                        date=date_info['date'],
                        movies_id=booking_pb2.MovieList(movies_id=date_info['movies'])
                    )
                    user_bookings.append(user_booking)

        return booking_pb2.BookingList(bookings=user_bookings)

    def AddBooking(self, request, context) -> booking_pb2.Empty:
        userid = request.userid  
        date = request.date  
        movies = list(request.movies_id.movies_id)  

        print("Movies:", movies)
        print("Date:", date)
        print("UserID:", userid)
        
        user_found = False
        for booking in self.db:
            if booking['userid'] == userid:
                user_found = True
                date_exists = False
                for existing_date in booking['dates']:
                    if existing_date['date'] == date:
                        for movie in movies:
                            if movie not in existing_date['movies']:
                                existing_date['movies'].append(movie)
                        date_exists = True
                        break
                if not date_exists:
                    print("Nouvelle date ajoutée:", date)
                    print("Films ajoutés:", movies)
                    booking['dates'].append({
                        'date': date,
                        'movies': movies
                    })
                break
        
        if not user_found:
            print("Nouvel utilisateur ajouté:", userid)
            print("Date ajoutée:", date)
            print("Films ajoutés:", movies)
            new_user_booking = {
                'userid': userid,
                'dates': [
                    {
                        'date': date,
                        'movies': movies
                    }
                ]
            }
            self.db.append(new_user_booking)

        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump({'bookings': self.db}, jsf, indent=4)

        return booking_pb2.Empty()




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3005')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

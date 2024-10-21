import grpc
from concurrent import futures
import time_pb2
import time_pb2_grpc
import json

class TimeServicer(time_pb2_grpc.TimeServicer):

    def __init__(self):
        with open('data/times.json', "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def GetTimes(self, request, context):
        schedule = time_pb2.Schedule()
        for entry in self.db:
            time_data = time_pb2.TimeData()
            time_data.date.date = entry['date'] 
            for movie in entry['movies']:
                movie_id = time_pb2.MovieID()
                movie_id.id = movie  
                time_data.movies_id.movies_id.append(movie_id)  
            schedule.times.append(time_data)  
        return schedule  

    def ShowMovies(self, request, context):
        movie_list = time_pb2.MovieList()
        for date in self.db:
            if date['date'] == request.date:
                print("Date found!")
                for movie in date['movies']:
                    movie_id = time_pb2.MovieID()
                    movie_id.id = movie  
                    movie_list.movies_id.append(movie_id)  
                return movie_list  
        return time_pb2.MovieList()  

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    time_pb2_grpc.add_TimeServicer_to_server(TimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    print("gRPC server running on port 3002...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

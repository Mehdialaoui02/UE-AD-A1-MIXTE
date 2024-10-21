import grpc
import time_pb2
import time_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = time_pb2_grpc.TimeStub(channel)
        date_request = time_pb2.Date(date="20151130")  
        response = stub.ShowMovies(date_request)
        if response.date:
            print(f"Movies for {response.date}:")
            for movie in response.movies_id:
                print(f"Movie ID: {movie.id}")
        else:
            print("No movies found for this date.")

if __name__ == '__main__':
    run()

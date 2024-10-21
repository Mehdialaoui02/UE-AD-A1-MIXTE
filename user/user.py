# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from json import dump
from werkzeug.exceptions import NotFound

# CALLING gRPC requests


# CALLING GraphQL requests
# todo to complete
movie_url = "http://192.168.145.229:3001/graphql"  # Remplace par l'URL réelle du service Movie
app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route('/', methods=['GET'])
def index():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route('/json', methods=['GET'])
def json():
   res=make_response(jsonify(users),200)
   return res

@app.route("/users/<userid>", methods=['GET'])
def get_movie_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/adduser/<userid>", methods=['POST'])
def add_new_user(userid):
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 409)
    users.append(req)
    write(users)
    res = make_response(jsonify({"message": "User added"}), 200)
    return res

@app.route("/movie/<movieid>", methods=['GET'])
def get_movie_by_id(movieid):
    query = f"""
    query {{
        movie_with_id(_id: "{movieid}") {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
            }}
        }}
    }}
    """
    
    response = requests.post(
        movie_url,
        json={'query': query}
    )

    if response.status_code == 200:
        movie_data = response.json()
        if 'errors' in movie_data:
            return make_response(jsonify({"error": movie_data['errors']}), 400)
        return make_response(jsonify(movie_data['data']), 200)
    else:
        return make_response(jsonify({"error": "Failed to fetch movie data"}), 500)

@app.route("/movie/title/<path:title>", methods=['GET'])
def get_movie_by_title(title):

    query = f"""
    query {{
        movie_with_title(_title: "{title}") {{
            id
            title
            director
            rating
            actors {{
                id
                firstname
                lastname
            }}
        }}
    }}
    """


    response = requests.post(
        movie_url,
        json={'query': query}
    )

    if response.status_code == 200:
        movie_data = response.json()
        if 'errors' in movie_data:
            return make_response(jsonify({"error": movie_data['errors']}), 400)
        return make_response(jsonify(movie_data['data']), 200)
    else:
        return make_response(jsonify({"error": "Failed to fetch movie data"}), 500)

def write(users):
    print(type(json))  # Vérification si json est bien un module
    with open('./data/users.json', 'w') as f:
        dump({"users": users}, f)  # Assure-toi d'utiliser json.dump correctement

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

"""
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):
    def GetBookings(self, request, context):
        with open('data/bookings.json') as f:
            bookings = json.load(f)['bookings']
        user_bookings = [b for b in bookings if b['userid'] == request.userid]
        return booking_pb2.BookingResponse(bookings=user_bookings)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()


import grpc
from concurrent import futures
import times_pb2
import times_pb2_grpc
import json

class ShowtimeServicer(times_pb2_grpc.ShowtimeServicer):
    def GetTimes(self, request, context):
        with open('data/times.json') as f:
            schedule = json.load(f)['schedule']
        for item in schedule:
            if item['date'] == request.date:
                return times_pb2.TimesResponse(movies=item['movies'])
        return times_pb2.TimesResponse(movies=[])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    times_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()


# booking_service.py

import grpc
import times_pb2
import times_pb2_grpc

def get_times(date):
    with grpc.insecure_channel('times:3003') as channel:
        stub = times_pb2_grpc.ShowtimeStub(channel)
        response = stub.GetTimes(times_pb2.TimesRequest(date=date))
        return response.movies


"""
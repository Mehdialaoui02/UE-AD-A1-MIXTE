from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from json import dump
from werkzeug.exceptions import NotFound

# GraphQL requests configuration
movie_url = "http://127.0.0.1:3001/graphql"  # Replace with the actual Movie service URL
app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route('/', methods=['GET'])
def index() -> str:
    """Welcome endpoint."""
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>", 200)

@app.route('/json', methods=['GET'])
def json() -> jsonify:
    """Return all users in JSON format."""
    res = make_response(jsonify(users), 200)
    return res

@app.route("/users/<userid>", methods=['GET'])
def get_movie_byid(userid: str) -> jsonify:
    """Retrieve a user by user ID."""
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)

@app.route("/adduser/<userid>", methods=['POST'])
def add_new_user(userid: str) -> jsonify:
    """Add a new user."""
    req = request.get_json()
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User ID already exists"}), 409)
    users.append(req)
    write(users)
    res = make_response(jsonify({"message": "User added"}), 200)
    return res

@app.route("/movie/<movieid>", methods=['GET'])
def get_movie_by_id(movieid: str) -> jsonify:
    """Retrieve a movie by its ID."""
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
def get_movie_by_title(title: str) -> jsonify:
    """Retrieve a movie by its title."""
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

@app.route("/addmovie", methods=['POST'])
def add_movie():
    """Handle POST request to add a new movie via GraphQL mutation."""
    # Get JSON data from the request body
    movie_data = request.get_json()

    if not movie_data:
        return jsonify({"error": "No data provided"}), 400

    # Prepare the GraphQL mutation
    mutation = f"""
        mutation Add_movie {{
            add_movie(_movie: {{
                id: "{movie_data['id']}",
                title: "{movie_data['title']}",
                director: "{movie_data['director']}",
                rating: {movie_data['rating']}
            }}) {{
                id
                title
                director
                rating
            }}
        }}
        """

    # Send the GraphQL mutation request
    response = requests.post(
        movie_url,
        json={'query': mutation},
    )

    # Check the response from the GraphQL service
    if response.status_code == 200:
        movie_data = response.json()
        if 'errors' in movie_data:
            return jsonify({"error": movie_data['errors']}), 400
        return jsonify(movie_data['data']), 200
    else:
        return jsonify({"error": "Failed to add movie, server responded with an error."}), response.status_code
    
@app.route("/delete/<movieid>", methods=['DELETE'])
def delete_movie(movieid):
    """Handle DELETE request to delete a movie via GraphQL mutation."""

    # Prepare the GraphQL mutation
    mutation = f"""
        mutation Delete_movie_by_id {{
            delete_movie_by_id(_id: "{movieid}") {{
                id
                title
                director
                rating
            }}
        }}
        """

    response = requests.post(
        movie_url,
        json={'query': mutation},
    )

    # Check the response from the GraphQL service
    if response.status_code == 200:
        movie_data = response.json()
        if 'errors' in movie_data:
            return jsonify({"error": movie_data['errors']}), 400
        return jsonify(movie_data['data']), 200
    else:
        return jsonify({"error": "Failed to delete movie, server responded with an error."}), response.status_code


def write(users: list) -> None:
    """Write the updated user data back to the JSON file."""
    with open('./data/users.json', 'w') as f:
        dump({"users": users}, f)  # Ensure proper JSON dump

if __name__ == "__main__":
    print("Server running on port %s" % PORT)
    app.run(host=HOST, port=PORT)
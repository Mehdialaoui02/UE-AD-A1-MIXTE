import json

def movie_with_id(_, info: str, _id: int) -> dict:
    """Retrieve a movie by its ID."""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate(_, info: str, _id: int, _rate: float) -> dict:
    """Update the rating of a movie by its ID."""
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def resolve_actors_in_movie(movie: dict, info: str) -> list:
    """Retrieve actors in a given movie."""
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        return [actor for actor in actors['actors'] if movie['id'] in actor['films']]

def movie_with_title(_, info: str, _title: str) -> dict:
    """Retrieve a movie by its title."""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

def delete_movie_by_id(_, info: str, _id: str) -> dict:
    """Delete a movie by its ID."""
    with open('./data/movies.json', "r") as dfile:
        data = json.load(dfile)

        # Vérifier si data est une liste ou un dictionnaire
        if isinstance(data, list):
            movies = data
        elif isinstance(data, dict) and "movies" in data:
            movies = data["movies"]
        else:
            raise ValueError("Unexpected data format in movies.json")

        # Supprimer le film correspondant à l'ID
        for movie in movies:
            if str(movie['id']) == str(_id):
                movies.remove(movie)
                # Écrire les changements dans le fichier JSON
                with open('./data/movies.json', "w") as dfile:
                    json.dump(data, dfile, indent=4)
                print("Movie removed:", movie)
                return movie

    print("Movie not found with id:", _id)
    return {}


def write(movies: list) -> None:
    """Write updated movies to the JSON file."""
    with open('{}/data/movies.json'.format("."), 'w') as f:
        json.dump(movies, f)

def add_movie(_, info: str, _movie: dict) -> dict:
    """Add a new movie if it doesn't already exist."""
    movieid = _movie['id']
    with open('{}/data/movies.json'.format("."), "r") as dfile:
        movies = json.load(dfile)['movies']
        for movie in movies:
            if movie["id"] == movieid:
                return {}
        movies.append(_movie)
        write(movies)
        return _movie

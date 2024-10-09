import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate(_,info,_id,_rate):
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

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result

def movie_with_title(_, info, _title) :
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

def delete_movie_by_id(_, info, _id) : 
    with open('{}/data/movies.json'.format("."), "r") as dfile:
        movies = json.load(dfile)['movies']
        for movie in movies :
            if movie['id'] == _id:
                movies.remove(movie)
                return movie


def write(movies):
    with open('{}/data/movies.json'.format("."), 'w') as f:
        json.dump(movies, f)

def add_movie(_, info, _movie):
    movieid = _movie['id']
    with open('{}/data/movies.json'.format("."), "r") as dfile:
        movies = json.load(dfile)['movies']
        for movie in movies:
            if movie["id"] == movieid:
                return {}
        movies.append(_movie)
        write(movies)
        return _movie





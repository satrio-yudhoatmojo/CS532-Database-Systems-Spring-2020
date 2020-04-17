from flask import Flask, render_template, request
from flask_pymongo import PyMongo

import utils


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello World, This is Me!'

@app.route('/movies')
def show_movies():
    '''Displays all movies in the dataset.'''

    # Query 'movie_title' attribute from 'movies' collection
    movies = mongo.db.movies.find({}, {'_id': 0, 'movie_title': 1})

    years = utils.get_year_list()

    genres = utils.get_genre_list()

    ratings = utils.enumerate_rating_range()

    # Send the query result to movies.html
    return render_template("movies.html", movies=movies, years=years, genres=genres, ratings=ratings)

@app.route('/actors')
def show_actors():
    '''Displays all actors in the dataset'''

    # Query 'actor_1_name', 'actor_2_name', and 'actor_3_name' from movies collection
    actors = mongo.db.movies.find({}, {'_id': 0, 'actor_1_name': 1, 'actor_2_name': 1, 'actor_3_name': 1})

    actor = []

    result = {}

    for items in actors:
        if items['actor_1_name'] not in actor:
            actor.append(items['actor_1_name'])

        if items['actor_2_name'] not in actor:
            actor.append(items['actor_2_name'])

        if items['actor_3_name'] not in actor:
            actor.append(items['actor_3_name'])

    actor.sort()

    for person in actor:
        # Count movies starred by the actor
        movie_count = mongo.db.movies.find({'$or': [{'actor_1_name': person}, {'actor_2_name': person}, {'actor_3_name': person}]}, {'_id': 0, 'movie_title': 1}).count()

        # Stores the count to result dictionary
        result[person] = movie_count

    return render_template("actors.html", actors=result)

@app.route('/movies_on_genres', methods=['GET', 'POST'])
def show_movies_on_genres():
    '''Get a list of movies based on certain genre.'''
    if request.method == 'POST':
        # Query list of movies genres for user to pick
        genres = utils.get_genre_list()

        # Query list of movies years for user to pick
        years = utils.get_year_list()

        year = request.form.get('years')
        genre = request.form.get('genres')

        substr = '^' + genre + '*'

        movies = mongo.db.movies.find({'genres': {'$regex': substr}, 'title_year': year})
        for i in movies:
            print(i)

        # data = utils.get_movies_on_genres(genre, year)
        data = []

        # Render the page
        return render_template("movies_on_genres.html", years=years, genres=genres, data=data)

    else:
        '''
        This is 'else' condition is for base case condition.
        The first time user open the page and has not picked any genre.
        '''
        # Query list of movies genres for user to pick
        genres = utils.get_genre_list()

        # Query list of movies years for user to pick
        years = utils.get_year_list()

        # Set data to None because we haven't retrieved any data yet
        data = None

        # Render the page
        return render_template("movies_on_genres.html", years=years, genres=genres, data=data)




if __name__ == '__main__':
    app.run()

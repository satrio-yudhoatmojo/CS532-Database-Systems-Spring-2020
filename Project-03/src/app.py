from flask import Flask, render_template, request, send_file
from flask_pymongo import PyMongo

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

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

# DONE
@app.route('/movies_on_year', methods=['GET', 'POST'])
def show_movies_on_year():
    '''Displays all movies in certain year.'''

    # Get list of years
    years = utils.get_year_list()

    if request.method == 'POST':
        year = request.form.get('years')

        # Querying movies on that year
        data = utils.get_movies_on_year(year)

        return render_template("query1.html", years=years, year=year, data=data)

    else:

        # Send the list of years to query1.html
        return render_template("query1.html", years=years)

# DONE
@app.route('/movies_on_genres', methods=['GET', 'POST'])
def show_movies_on_genres():
    '''Get a list of movies based on certain genre.'''

    # Query list of movies genres for user to pick
    genres = utils.get_genre_list()

    # Query list of movies years for user to pick
    years = utils.get_year_list()

    if request.method == 'POST':

        # Get POST data
        year = request.form.get('years')
        genre = request.form.get('genres')

        data = utils.get_movies_on_genres(genre, year)

        # Render the page
        return render_template("query2.html", year=year, genre=genre, years=years, genres=genres, data=data)

    else:
        '''
        This is 'else' condition is for base case condition.
        The first time user open the page and has not picked any genre.
        '''

        # Render the page
        return render_template("query2.html", years=years, genres=genres)

# DONE
@app.route('/actors')
def show_actors():
    '''Displays all actors in the dataset'''

    # Query list of actors and the number of movies they starred in
    actors = utils.get_actors()

    return render_template("query3.html", actors=actors)

# DONE
@app.route('/movies_on_ratings', methods=['GET', 'POST'])
def show_movies_on_ratings():
    '''Display list of movies based on a range of ratings.'''

    years = utils.get_year_list()

    if request.method == 'POST':
        # Get POST data
        year = request.form.get('years')
        lower_bound = request.form.get('lower_bound')
        upper_bound = request.form.get('upper_bound')

        # Query a list of movies on specific year within a specific range of ratings
        data = utils.get_movies_on_rating_range(lower_bound, upper_bound, year)

        return render_template("query7.html", years=years, year=year,lower_bound=lower_bound, upper_bound=upper_bound, data=data)
    else:

        return render_template("query7.html", years=years)

@app.route('/movies_revenues', methods=['GET', 'POST'])
def show_movies_revenues():
    '''Displays yearly average budget and gross revenue of all movies.'''

    if request.method == 'POST':
        year = request.form.get('years')
        # Querying the yearly average budget and gross revenue of all movies
        query = mongo.db.movies.aggregate([{"$match": {"title_year": year}},
                                          {"$group": {"_id": "$movie_title",
                                                      "avg_budget": {"$avg": "$budget"},
                                                      "avg_gross": {"$avg": "$gross"}}}])

        movie = []
        datatype = []
        average = []
        data = {}

        for i in query:
            movie.append(i['_id'])
            movie.append(i['_id'])
            datatype.append('budget')
            datatype.append('gross')
            average.append(i['avgBudget'])
            average.append(i['avgGross'])

        data['movie'] = year
        data['type'] = datatype
        data['average'] = average

        # Pandas dataframe
        df = pd.DataFrame(data)

        # Making of the chart
        sns.set(style="whitegrid")

        # Create factorplot barchart
        sns.factorplot(x="movie", y="average", hue="type", data=df, kind="bar")

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)

        return send_file(bytes_image, attachment_filename='plot.png', mimetype='image/png')
    else:
        years = utils.get_year_list()

        return render_template("movies_revenues.html", years=years)

@app.route('/top_ten_movies', methods=['GET', 'POST'])
def show_top_ten_movies():
    '''Display top ten movies on certain year.'''

    if request.method == 'POST':
        pass
    else:
        years = utils.get_year_list()

    return render_template("top_ten_movies.html", years=years)







if __name__ == '__main__':
    app.run()

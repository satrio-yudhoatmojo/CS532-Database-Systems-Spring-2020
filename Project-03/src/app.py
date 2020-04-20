from flask import Flask, render_template, request, send_file
from flask_pymongo import PyMongo

import utils


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/movies"
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template("index.html")

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
@app.route('/top_ten_movies', methods=['GET', 'POST'])
def show_top_ten_movies():
    '''Display top ten movies on certain year.'''

    years = utils.get_year_list()

    if request.method == 'POST':
        # Get POST data
        year = request.form.get('years')

        data = utils.get_top_ten_movies_on_year(year)

        # Preparing data for the chart
        legend = "Top Movies in Year" + year
        labels = data['movies']
        values = data['imdb_scores']

        return render_template("query4.html", year=year, years=years, legend=legend, labels=labels, values=values)
    else:

        return render_template("query4.html", years=years)

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

# TODO: Graph is not working
@app.route('/movies_revenues')
def show_movies_revenues():
    '''Displays yearly average budget and gross revenue of all movies.'''

    # Querying the yearly average budget and gross revenue of all movies
    data = utils.get_budget_vs_gross_movies()

    labels = data['years']
    avg_budget = data['avg_budget']
    avg_gross = data['avg_gross']

    return render_template("query6.html", labels=labels, avg_budget=avg_budget, avg_gross=avg_gross)

@app.route('/movies_rating_vs_revenue', methods=['GET', 'POST'])
def show_movies_rating_vs_revenue():
    '''Display movies rating vs movies revenue on specific year.'''

    years = utils.get_year_list()

    if request.method == 'POST':
        # Get POST data
        year = request.form.get('years')
        print(year)

        data = utils.get_rating_vs_gross_movies(year)

        labels = data['movies']
        imdb_score = data['imdb_score']
        gross = data['gross']

        return render_template("query5.html", years=years, year=year, labels=labels, imdb_score=imdb_score, gross=gross)


    else:
        return render_template('query5.html', years=years)

@app.route('/genres_timeline')
def show_genres_timelline():
    data = utils.get_genre_timeline()

    return render_template("query8.html", data=data)
if __name__ == '__main__':
    app.run()

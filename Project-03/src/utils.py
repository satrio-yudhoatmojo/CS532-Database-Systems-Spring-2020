from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.movies

def get_year_list():
    '''Get unique list of movie years.'''

    # Initializing result list for storing the result
    result = []

    # Querying 'title_year' from 'movies' collection
    years = db.movies.distinct('title_year')

    # Storing the result into result list and
    # casting the returned value into integer
    # somehow the dataset stored the 'title_year' in double data type
    for year in years:
        result.append(int(year))

    # return result
    return result

def get_genre_list():
    '''Get a list of movie genres.'''

    # Initializing result list
    result = []

    # Querying 'genres' from 'movies' collection
    genres = db.movies.find({},{'_id': 0, 'genres': 1})

    # Iterating to each query result
    for genre in genres:
        # Genres stored in the dataset has this format: genre1|genre2|genre3
        # Therefore, we need to split the result and stored them in result list
        items = genre['genres'].split('|')

        # Iterating to the result of splitting the query result
        for item in items:
            # Stores only unique genre
            if item not in result:
                # Append the item to the result list
                result.append(item)

    return result

def enumerate_rating_range():
    '''
    Get a list of rating range.
    This is used as a parameter to get list of movies based on ratings.
    User will input a range of movie ratings.
    '''
    ratings = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

    return ratings

def get_movies_on_rating_range(low_range, high_range, year):
    '''Get list of movies based on a range of ratings.'''

    # Querying the movies
    movies = db.movies.find({'imdb_score': {'$gte': low_range, '$lte': high_range}, 'title_year': year}).sort({'imdb_score': -1})

    return movies

def get_movies_on_genres(genre, year):
    '''Get list of movies based on a certain genre.'''

    str = '^' + genre + '*'
    print(str)
    print(year)

    # Querying the movies
    movies = db.movies.find({'genres': {'$regex': str}, 'title_year': year})

    for i in movies:
        print(i['movie_title'])

    return movies


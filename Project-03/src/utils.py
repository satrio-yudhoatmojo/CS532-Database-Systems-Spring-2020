from pymongo import MongoClient

client = MongoClient()
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

def get_movies_on_year(year):
    '''Get a list of movies on a specific year.'''

    # Querying to database
    movies = db.movies.find({'title_year': int(year)},
                                {'_id': 0, 'movie_title': 1, 'director_name': 1, 'content_rating': 1, 'duration': 1,
                                 'language': 1,
                                 'country': 1, 'genres': 1, 'imdb_score': 1})
    result = {}

    for i in movies:
        result[i['movie_title']] = {'movie_title': i['movie_title'],
                                    'director_name': i['director_name'],
                                    'content_rating': i['content_rating'],
                                    'duration': i['duration'],
                                    'language': i['language'],
                                    'country': i['country'],
                                    'genres': i['genres'],
                                    'imdb_score': i['imdb_score']}

    return result

def get_movies_on_genres(genre, year):
    '''Get list of movies based on a certain genre.'''

    reg_exp = '^' + genre + '*'
    print(reg_exp)

    # Querying the movies
    data = db.movies.find({'genres': {'$regex': reg_exp}, 'title_year': year}, {'_id': 0, 'movie_title': 1})

    print(data)
    for i in data:
        print(i['movie_title'])


    return data

def get_actors():
    # Query 'actor_1_name', 'actor_2_name', and 'actor_3_name' from movies collection
    actors = db.movies.find({}, {'_id': 0, 'actor_1_name': 1, 'actor_2_name': 1, 'actor_3_name': 1})

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
        movie_count = db.movies.find(
            {'$or': [{'actor_1_name': person}, {'actor_2_name': person}, {'actor_3_name': person}]},
            {'_id': 0, 'movie_title': 1}).count()

        # Stores the count to result dictionary
        result[person] = {'actor_name': person, 'movie_count': movie_count}

    return result



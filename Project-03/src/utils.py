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
    data = db.movies.find({"genres": {"$regex": reg_exp}, "title_year": int(year)}).sort("movie_title")

    result = {}

    for i in data:
        result[i['movie_title']] = {'movie_title': i['movie_title'],
                                    'director_name': i['director_name'],
                                    'content_rating': i['content_rating'],
                                    'duration': i['duration'],
                                    'language': i['language'],
                                    'country': i['country'],
                                    'genres': i['genres'],
                                    'imdb_score': i['imdb_score']}

    return result


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

def get_top_ten_movies_on_year(year):
    '''Get a list of top ten highest rated movies on a certain year.'''

    data = db.movies.find({"title_year": int(year)}).sort("imdb_score", -1).limit(10)

    movies = []
    imdb_scores = []
    result = {}

    for i in data:
        movies.append(i['movie_title'])
        imdb_scores.append(i['imdb_score'])

    result['movies'] = movies
    result['imdb_scores'] = imdb_scores

    return result

def get_budget_vs_gross_movies():
    '''Get budget and gross revenue data of movies on specific year.'''

    #data = db.movies.aggregate([{"$match": {"title_year": year}},
    #                                     {"$group": {"_id": "$movie_title",
    #                                                  "avg_budget": {"$avg": "$budget"},
    #                                                  "avg_gross": {"$avg": "$gross"}}}])

    #data = db.movies.aggregate([{"$group": {"_id": "$title_year", "min": {"$min": "$budget"}, "avg": {"$avg": "$budget"}, "max": {"$max": "$budget"}}}, {"$sort": {"_id": 1}}])

    data = db.movies.aggregate([{"$group": {"_id": "$title_year", "avg_budget": {"$avg": "$budget"}, "avg_gross": {"$avg": "$gross"}}}, {"$sort": {"_id": 1}}])

    years = []
    avg_budget = []
    avg_gross = []

    result = {}

    for i in data:
        years.append(i['_id'])
        avg_budget.append(i['avg_budget'])
        avg_gross.append(i['avg_gross'])

    result['years'] = years
    result['avg_budget'] = avg_budget
    result['avg_gross'] = avg_gross

    return result

def get_movies_on_rating_range(low_range, high_range, year):
    '''Get list of movies based on a range of ratings.'''

    # Querying the movies
    movies = db.movies.find({"imdb_score": {"$gte": float(low_range), "$lte": float(high_range)}, "title_year": int(year)})

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

    return movies

def get_rating_vs_gross_movies(year):
    '''Get movie rating data and gross income data for all movies on specific year.'''

    data = db.movies.find({'title_year': int(year)})

    movies = []
    imdb_score = []
    gross = []

    result = {}

    for i in data:
        movies.append(i['movie_title'])
        imdb_score.append(i['imdb_score'])
        gross.append(i['gross'])

    result['movies'] = movies
    result['imdb_score'] = imdb_score
    result['gross'] = gross

    return result

def get_genre_timeline():
    '''Get number of movies on each genre throughout the time.'''

    # Get a list of movie genres
    genres = get_genre_list()

    result = {}

    for genre in genres:
        reg_ex = '^' + genre + '*'

        data = db.movies.aggregate([{"$match": {"genres": {"$regex": reg_ex}}},{"$group": {"_id": "$title_year", "count": {"$sum": 1}}},{"$sort": {"_id": 1}}])

        result[genre] = {}

        for i in data:
            result[genre][i['_id']] = i['count']

    print(result)
    return result
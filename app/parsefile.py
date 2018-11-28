import json
from datetime import datetime
import time
import urllib.parse
import requests
from .db import *
from environment import API_KEY

MAX_TRIES = 3
API_SLEEP_TIME = 10

class Movie:

    def __init__(self, name, runtime, times_watched = 1):
        self.name = name
        self.runtime = runtime
        self.times_watched = times_watched


class Series:

    def __init__(self, name, runtime, episodes_watched = 1):
        self.name = name
        self.runtime = runtime
        self.episodes_watched = episodes_watched


def parse_title(title):
    title = title.replace("’", "'")
    title = title.replace("(U.S.)", "")
    title = title.replace("(U.K.)", "")
    return urllib.parse.quote_plus(title)


def get_media_runtime(most_probable_result):
    media = requests.get("https://api.themoviedb.org/3/" +
                         most_probable_result['media_type'] +
                         "/" +
                         str(most_probable_result['id']) +
                         "?api_key=" +
                         API_KEY +
                         "&language=en-US")
    if media.status_code == 7:
        print("INVALID API KEY")
    try:
        runtime = 0
        if most_probable_result['media_type'] == 'movie':
            runtime = media.json()['runtime']
        elif most_probable_result['media_type'] == 'tv':
            runtime = media.json()['episode_run_time'][0]
            if len(media.json()['episode_run_time']) > 1:
                print("multiple runtimes")

        return runtime
    except (IndexError, KeyError):
        print("Runtime Duration not found for title: " + most_probable_result['name'])
        return 0


def try_search_tmdb(title):
    tries = 1
    while tries < MAX_TRIES:
        tries += 1
        result = requests.get("https://api.themoviedb.org/3/search/multi?" +
                              "api_key=" + API_KEY + "&language=en-US&query=" +
                              title + "&page=1&include_adult=false")

        if result.status_code == 200:
            return result
        elif result.status_code == 429:
            time.sleep(API_SLEEP_TIME)


def parse_file(items):

    series = {}
    movies = {}
    tot_length = 0
    not_found = 0
    no_of_movies = 0
    data = {}
    dates = {}
    weekdays = [0] * 7
    months = [0] * 13
    years = {}

    for title in items:
        #print(title)
        date = datetime.strptime(items[title], '%Y-%m-%d')
        title = parse_title(list(title.split(':'))[0])
        if date not in dates:
            dates[date] = 0
        if date.year not in years:
            years[date.year] = 0

        if title in series:
            JSONMedia = series[title]
            JSONMedia.episodes_watched += 1
            series[title] = JSONMedia
            dates[date] += JSONMedia.runtime
            years[date.year] += JSONMedia.runtime
            tot_length += JSONMedia.runtime
            weekdays[date.weekday()] += JSONMedia.runtime
            months[date.month - 1] += JSONMedia.runtime
            continue

        if title in movies:
            JSONMedia = movies[title]
            JSONMedia.times_watched += 1
            movies[title] = JSONMedia
            dates[date] += JSONMedia.runtime
            years[date.year] += JSONMedia.runtime
            tot_length += JSONMedia.runtime
            weekdays[date.weekday()] += JSONMedia.runtime
            months[date.month - 1] += JSONMedia.runtime
            continue

        media = get_media(title)
        if media:
            runtime = media.runtime
            if media.movie == 1:
                no_of_movies += 1
                movies[title] = Movie(title, runtime)
            elif media.movie == 0:
                series[title] = Series(title, runtime)
            else:
                print("Type not found of: " + title)

            dates[date] += runtime
            years[date.year] += runtime
            tot_length += runtime
            weekdays[date.weekday()] += runtime
            months[date.month - 1] += runtime
            continue

        search = try_search_tmdb(title)

        if len(list(search.json()['results'])) > 0:
            most_probable_result = list(search.json()['results'])[0]
            runtime = get_media_runtime(most_probable_result)
            if most_probable_result['media_type'] == 'movie':
                no_of_movies += 1
                add_media(title, runtime, 1)
                movies[title] = Movie(title, runtime)

            else:
                add_media(title, runtime, 0)
                series[title] = Series(title, runtime)

        else:
            if title == "Club+of+Crows":
                runtime = 40
                series[title] = Series(title, runtime)
            else:
                add_notfound(title)
                print("Not found: {}".format(title))
                not_found += 1

        dates[date] += runtime
        years[date.year] += runtime
        weekdays[date.weekday()] += runtime
        months[date.month - 1] += runtime
        tot_length += runtime

    longest_time = max(dates.values())
    longest_day = max(dates, key=(lambda key: dates[key]))
    top_series = max(series, key=(lambda key: (series[key].episodes_watched * series[key].runtime)))
    top_movie = max(movies, key=(lambda key: movies[key].times_watched))

    data['runtime'] = tot_length
    data['not_found'] = not_found
    data['movies'] = no_of_movies
    data['highscore'] = longest_time
    data['highscore_date'] = str(longest_day).split(' ')[0]
    data['top_series'] = urllib.parse.unquote_plus(top_series)
    data['top_series_episodes'] = series[top_series].episodes_watched
    data['top_series_total_time'] = (series[top_series].episodes_watched * series[top_series].runtime)/60
    data['top_movie'] = urllib.parse.unquote_plus(top_movie)
    data['top_movie_times'] = movies[top_movie].times_watched
    # Convert to hours
    data['weekdays'] = list(map((lambda x: x/60), weekdays))
    data['months'] = list(map((lambda x: x/60), months))
    data['years'] = years
    return json.dumps(data)


def test_db():
    add_media('test', 5, 0)
    media = get_media('test')
    delete_media('test')
    return media.runtime


def show_db():
    allt = get_all()
    print(list(allt))
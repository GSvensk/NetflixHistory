from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import urllib.parse
import time
from flask_cors import CORS


API_KEY = "8"
MAX_TRIES = 3
API_SLEEP_TIME = 10

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

    try:
        runtime = 0
        if most_probable_result['media_type'] == 'movie':
            runtime =  media.json()['runtime']
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
                              "api_key=8c04c3e5fe547c0b2ec18438737a5dbc&language=en-US&query=" +
                              title + "&page=1&include_adult=false")

        if result.status_code == 200:
            return result
        elif result.status_code == 429:
            time.sleep(API_SLEEP_TIME)


app = Flask(__name__)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()

class ParseFile(Resource):
    def post(self):
        #parser.add_argument('items')
        parser.add_argument("items", type=dict, action="append")

        args = parser.parse_args()
        items = args['items'][0]

        media_length = {}
        dates = {}
        tot_length = 0
        not_found = 0
        titles_consumed = 0

        for title in items:
            print(title)
            date = items[title]
            title = parse_title(list(title.split(':'))[0])
            dates[date] = 0

            titles_consumed += 1

            if title in media_length:
                dates[date] += media_length[title]
                tot_length += media_length[title]
                continue

            search = try_search_tmdb(title)

            if len(list(search.json()['results'])) > 0:

                most_probable_result = list(search.json()['results'])[0]
                runtime = get_media_runtime(most_probable_result)
                dates[date] += runtime
                media_length[title] = runtime
                tot_length += runtime

            else:
                print("Not found: {}".format(title))
                not_found += 1

        print("Not found: " + str(not_found))
        print(tot_length)
        print(tot_length / 60)
        longest_time = max(dates.values())
        print("longest_time?" + str(longest_time))
        longest_day = max(dates.keys(), key=(lambda key: dates[key]))
        print("Top day: " + longest_day + " Length (h): " + str(dates[longest_day] / 60))

        return {'runtime': tot_length/60}


api.add_resource(ParseFile, '/parse')

if __name__ == '__main__':
    app.run(debug=True)
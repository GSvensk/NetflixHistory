import redis
import json
from environment import REDIS_HOSTNAME, REDIS_PASSWORD
from app.models import Movie, Series

class Media:

    def __init__(self, name, runtime, is_movie = True):
        self.name = name
        self.runtime = runtime
        self.is_movie = is_movie

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=1)


class Redis:
    r = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, password=REDIS_PASSWORD, ssl=False)

    def ping_cache(self):
        result = self.r.ping()
        print("Ping returned : " + str(result))
        return str(result)


    def getMedia(self, name):
        result = self.r.get(name)
        if not result:
            return None

        json_obj = result.decode("utf-8")
        decoded = json.loads(json_obj)
        if decoded["is_movie"]: 
            return Movie(name, decoded["runtime"], times_watched = 1)
        return Series(name, decoded["runtime"], episodes_watched = 1)


    def setMedia(self, name, runtime, is_movie = True):
        media = Media(name, runtime, is_movie).toJSON()
        result = self.r.set(name, media)
        if result == "False":
            print("Redis Cache set failed")



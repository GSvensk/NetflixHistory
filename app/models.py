import json

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

from init import db

class Media(db.Model):
    name = db.Column(db.String(80), primary_key=True, unique=False, nullable=False)
    runtime = db.Column(db.Integer(), unique=False, nullable=True)
    movie = db.Column(db.Integer())

    def __init__(self, name, runtime, mediatype = 0):
        self.name = name
        self.runtime = runtime
        self.mediatype = mediatype

    def __repr__(self):
        return 'Media {}'.format(self.name)


class NotFound(db.Model):
    name = db.Column(db.String(80), primary_key=True, unique=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'NotFound {}'.format(self.name)

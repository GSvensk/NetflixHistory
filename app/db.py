from init import db
from .models import Media, NotFound


def init_db():
    db.create_all()
    #Media.query.delete()
    db.session.commit()


def get_runtime(name):
    media = Media.query.filter_by(name=name).first()
    if media:
        return media.runtime
    else:
        return -1


def add_media(name, runtime, mediatype = 0):
    media = Media(name, runtime, mediatype)
    db.session.add(media)
    db.session.commit()


def add_notfound(name):
    not_found = NotFound.query.filter_by(name=name).first()
    if not not_found:
        not_found = NotFound(name)
        db.session.add(not_found)
        db.session.commit()


def delete_media(name):
    db.session.delete(Media.query.filter_by(name=name).first())
    db.session.commit()


def get_all():
    return Media.query.all()
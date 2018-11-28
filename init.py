from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/parse": {"origins": "*"}})
api = Api(app)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

parser = reqparse.RequestParser()

class ParseFile(Resource):
    def post(self):
        parser.add_argument("items", type=dict, action="append")
        args = parser.parse_args()
        items = args['items'][0]
        from app.parsefile import parse_file
        json_data = parse_file(items)
        return json_data


class TestDB(Resource):
    def get(self):
        from app.parsefile import test_db
        with app.app_context():
            return test_db()


class ShowDB(Resource):
    def get(self):
        from app.parsefile import show_db
        with app.app_context():
            return show_db()


api.add_resource(ParseFile, '/parse')
api.add_resource(TestDB, '/test')
api.add_resource(ShowDB, '/show')


if __name__ == '__main__':
    from app.db import init_db
    init_db()
    app.run(debug=True)


@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()
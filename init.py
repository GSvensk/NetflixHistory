from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/parse": {"origins": "*"}})
api = Api(app)
#if local
#file_path = os.path.abspath(os.getcwd())+"\database.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
#if prod?
#DATABASE_URL = os.environ['DATABASE_URL']
#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oahgefuyjsvlfw:3091468ced69d00e2b861e50f69c89dbdbe5543e04f0fb0b18574fafd31f8f7b@ec2-54-75-231-3.eu-west-1.compute.amazonaws.com:5432/dd1ca7tqpk39v8'
db = SQLAlchemy(app)
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
    #from app.db import init_db
    #init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)


@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()
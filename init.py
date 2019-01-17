from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/parse": {"origins": "*"}})
api = Api(app)

parser = reqparse.RequestParser()

class ParseFile(Resource):
    def post(self):
        parser.add_argument("items", type=dict, action="append")
        args = parser.parse_args()
        items = args['items'][0]
        from app.parsefile import parse_file
        json_data = parse_file(items)
        return json_data


api.add_resource(ParseFile, '/parse')


if __name__ == '__main__':
    from app.db import recreate_tables
    #recreate_tables()

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

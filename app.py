from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.book import Book, BookList
from resources.library import Library, LibraryList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'John'
api = Api(app)

# JWT creates a new end-point /auth
jwt = JWT(app, authenticate, identity)

api.add_resource(Library, '/library/<string:library_name>')
api.add_resource(Book, '/book/<string:book_name>')
api.add_resource(BookList, '/books')
api.add_resource(UserRegister, '/register')
api.add_resource(LibraryList, '/libraries')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3000, debug=True)

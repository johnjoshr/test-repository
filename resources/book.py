import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.book import BookModel

class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('location',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )

    parser.add_argument('library_id',
                        type=int,
                        required=True,
                        help='Every book needs a library_id'
                        )

    @jwt_required()
    def get(self, book_name):
        book = BookModel.does_book_exist(book_name)
        if book:
            return book.json()
        return {'message': 'Book not found in the database'}, 404

    def post(self, book_name):
        if BookModel.does_book_exist(book_name):
            # 400 - bad request
            return {'message': 'A book with name {} already exists'.format(book_name)}, 400

        request_data = Book.parser.parse_args()
        #request_data = request.get_json() # force = True - Means donot need content type header. silent=True - does not give error, but returns none

        book = BookModel(book_name, **request_data)
        try:
            book.save_book_info()
        except:
            return {'message': 'Error occured during insert'}, 500

        return book.json(), 201  # 201 is for object is created

    def delete(self, book_name):
        book = BookModel.does_book_exist(book_name)

        if book:
            book.delete_book_info()
            return {'message': 'Book {} deleted'.format(book_name)}, 200
        else:
            return {'message': 'The book does not exist'}

    def put(self, book_name):
        request_data = Book.parser.parse_args()

        book = BookModel.does_book_exist(book_name)

        if book:
            book.location = request_data['location']
        else:
            book = BookModel(book_name, **request_data)

        book.save_book_info()

        return book.json()


class BookList(Resource):
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}
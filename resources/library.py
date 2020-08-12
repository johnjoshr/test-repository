from flask_restful import Resource
from models.library import LibraryModel

class Library(Resource):

    def get(self, library_name):
        library = LibraryModel.does_library_exist(library_name)
        if library:
            return library.json(), 200
        return {'message': 'Library Not found'}, 404

    def post(self, library_name):
        if LibraryModel.does_library_exist(library_name):
            return {'message': 'Library already exists'}, 400

        library = LibraryModel(library_name)

        try:
            library.save_library_info()
        except:
            return {'message': 'An error occured while creating store'}, 500

        return library.json(), 201
        
    def delete(self, library_name):
        library = LibraryModel.does_library_exist(library_name)
        if library:
            library.delete_library_info()
        
        return {'message': 'Library deleted'}


class LibraryList(Resource):
    def get(self):
        return {'libraries': [library.json() for library in LibraryModel.query.all()]}
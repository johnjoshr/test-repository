from db import db

class LibraryModel(db.Model):

    __tablename__ = 'LIBRARY'

    id = db.Column(db.Integer, primary_key=True)
    library_name = db.Column(db.String(100))

    books = db.relationship('BookModel', lazy='dynamic')

    def __init__(self, library_name):
        self.library_name = library_name

    def json(self):
        return {'library_name': self.library_name, 'books': [book.json() for book in self.books.all()]}

    @classmethod
    def does_library_exist(cls, library_name):
        return cls.query.filter_by(library_name=library_name).first()

    def save_library_info(self):
        db.session.add(self)
        db.session.commit()

    def delete_library_info(self):
        db.session.delete(self)
        db.session.commit()
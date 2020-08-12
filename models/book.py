from db import db

class BookModel(db.Model):
    
    __tablename__ = 'BOOKS'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    location = db.Column(db.String(30))

    library_id = db.Column(db.Integer, db.ForeignKey('LIBRARY.id'))
    library = db.relationship('LibraryModel')

    def __init__(self, book_name, location, library_id):
        self.book_name = book_name
        self.location = location
        self.library_id = library_id

    def json(self):
        return {'book_name': self.book_name, 'location': self.location}

    @classmethod
    def does_book_exist(cls, book_name):
        return cls.query.filter_by(book_name=book_name).first()

    def save_book_info(self):
        db.session.add(self)
        db.session.commit()

    def delete_book_info(self):
        db.session.delete(self)
        db.session.commit()
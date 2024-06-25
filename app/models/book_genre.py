from app import db

class BookGenre(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    book = db.relationship('Book', back_populates='book_genres')
    genre = db.relationship('Genre', back_populates='book_genres')

    @classmethod
    def from_dict(cls, book_genre_dict):
        try:
            book_id = book_genre_dict['book_id']
            genre_id = book_genre_dict['genre_id']
            return cls(book_id=book_id, genre_id=genre_id)
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "genre_id": self.genre_id
        }
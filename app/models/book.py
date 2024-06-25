from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', back_populates='books')
    book_genres = db.relationship('BookGenre', back_populates='book')


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, book_dict):
        try:
            title = book_dict['title']
            description = book_dict['description']
            book = cls(title=title, description=description)
            return book
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")

from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship('Book', back_populates='author')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [{'id': book.id, 'title': book.title} for book in self.books]
        }

    @classmethod
    def from_dict(cls, data):
        if 'name' not in data:
            raise ValueError("Missing required field: name")
        return cls(name=data['name'])

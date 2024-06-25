from app import db


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    book_genres = db.relationship('BookGenre', back_populates='genre')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data):
        if 'name' not in data:
            raise ValueError("Missing required field: name")
        return cls(name=data['name'])
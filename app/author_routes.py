from app import db
from app.models.author import Author
from app.models.book import Book
from .helpers import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    try:
        new_author = Author.from_dict(request_body)

        db.session.add(new_author)
        db.session.commit()
        return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)
    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))

@authors_bp.route("/<author_id>", methods=["GET"])
def handle_one_author(author_id):
    author = validate_model(Author,author_id)
    author_dict = {"id": author.id, "name": author.name}

    return jsonify(author_dict), 200


@authors_bp.route("", methods=["GET"])
def read_all_authors():
    authors = Author.query.all()

    authors_response= [author.to_dict() for author in authors]

    return jsonify(authors_response)

#POST
@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_model(Author, author_id)
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body, author)
        new_book.author = author

        db.session.add(new_book)
        db.session.commit()
        
        return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))

#GET/authors/1/books
@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books(author_id):

    author = validate_model(Author, author_id)

    books_response = []
    for book in author.books:
        books_response.append(book.to_dict())

    return jsonify(books_response)
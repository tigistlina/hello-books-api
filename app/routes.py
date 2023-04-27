from app import db
from app.models.book import Book
from flask import Blueprint, jsonify,make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("",methods=["POST", "GET"])
def handle_books():
    if request.method == "POST":
        request_body= request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)
        new_book = Book(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        return make_response(
            f"Book {new_book.title} created.", 201
        )
    elif request.method == "GET":
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append(
                {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
                            )
        return jsonify(books_response), 200

# def validate_book(book_id):
#     # handle invalid book_id, return 400
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message": f"book {book_id} invalid"} , 400))
#     # search for book_id in data, return book
#     for book in books:
#         if book.id == book_id:
#             return book
#     # return 404 for non-existing book
#     abort(make_response({"message": f"book {book_id} not found"} , 404))


# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)
#     print(book)
#     return {
#             "id": book.id,
#             "title":book.title,
#             "description": book.description

#             }

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body
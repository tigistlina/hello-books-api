from flask import jsonify, make_response
import pytest

# get all books and return no records
def test_get_books_with_no_records(client):
    response = client.get('/books')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# When we have records, `read_all_books` returns a list containing a dictionary representing each `Book`
def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }

# When we have records and a `title` query in the request arguments, `read_all_books` returns a list containing only the `Book`s which match the query
def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {'title': 'Desert Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# When we have records and a `title` query in the request arguments, `read_all_books` returns a list containing only the `Book`s which match the query
def test_get_all_books_with_title_query_matching_one(client, two_saved_books):
    # Act
    data = {'title': 'Ocean Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

# When we call `read_one_book` with a numeric ID that doesn't have a record, we get the expected error message
def test_get_one_book_id_not_found(client, two_saved_books):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"book 3 not found"}

# When we call `read_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_book_id_invalid(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message":"book cat invalid"}

# get one book by id
def test_get_book_by_id(client, two_saved_books):
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        'id': 1,
        'title': 'Ocean Book',
        'description':'watr 4evr'

    }

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book created."

def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act & Assert
    # with pytest.raises(KeyError, match='title'):
    #     response = client.post("/books", json=test_data)
    # Act
    response = client.post("/books", json=test_data)

    # Assert
    assert response.status_code == 400
    assert "Invalid Request" in response.get_data(as_text=True)



def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act & Assert
    # with pytest.raises(KeyError, match = 'description'):
    #     response = client.post("/books", json=test_data)

    # Act
    response = client.post("/books", json=test_data)

    # Assert
    assert response.status_code == 400
    assert "Invalid Request" in response.get_data(as_text=True)

def test_create_one_book_with_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book created."

def test_delete_one_book(client, two_saved_books):
    #Act
    response = client.delete('/books/1')

    #Arrange
    response_body = response.get_data(as_text=True)

    #Assert
    assert response.status_code == 200
    assert response_body == "Book #1 successfully deleted"

def test_update_one_book(client, two_saved_books):
        #Act
    response = client.put('/books/1', json={
        "title": " Best Book",
        "description": "The Best Book!"
    })

    #Arrange
    response_body = response.get_data(as_text=True)

    #Assert
    assert response.status_code == 200
    assert response_body == "Book #1 successfully updated."
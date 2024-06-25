import pytest
from app.models.book import Book

def test_book_to_dict():
    # Arrange
    book = Book(id = 1, title="Ocean Book", description="watr 4evr")
    expected_dict = {
        "id": 1, # The id is autoincremented
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

    # Act
    book_dict = book.to_dict()

    # Assert
    assert book_dict == expected_dict

def test_book_from_dict():
    # Arrange
    book_dict = {
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }

    # Act
    book = Book.from_dict(book_dict)

    # Assert
    assert isinstance(book, Book)
    assert book.title == "Mountain Book"
    assert book.description == "i luv 2 climb rocks"

def test_book_from_dict_missing_description():
    # Arrange
    book_dict = {
        "title": "Ocean Book"
        # Missing 'description' field
    }

    # Act & Assert
    with pytest.raises(ValueError) as e:
        Book.from_dict(book_dict)


def test_book_from_dict_missing_title():
    # Arrange
    book_dict = {
        "description": "i luv 2 climb rocks"
        # Missing 'title' field
    }

    # Act & Assert
    with pytest.raises(ValueError) as e:
        Book.from_dict(book_dict)


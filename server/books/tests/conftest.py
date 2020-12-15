import pytest

from books.models import (
    Author,
    Book,
    Review
)


@pytest.fixture
def authors():
    for name in ('Anna Wolf', 'Suzanne Collins'):
        Author.objects.create(name=name)


@pytest.fixture
def books(authors):
    values = [
        {
            "isbn": "9788380087583",
            "title": "Ballada ptaków i węży",
            "genre": "Literatura młodzieżowa",
            "author_id": 1
        },
        {
            "isbn": "9788366553798",
            "title": "Osiedle RZNiW",
            "genre": "Kryminał",
            "author_id": 2
        }
    ]
    for book in values:
        Book.objects.create(**book)


@pytest.fixture
def reviews(books):
    values = [
                {
                    "rate": 3,
                    "description": "test1",
                    "book_id": 1
                },
                {
                    "rate": 3,
                    "description": "test2",
                    "book_id": 1
                },
                {
                    "rate": 4,
                    "description": "test3",
                    "book_id": 1
                }
            ]
    for review in values:
        Review.objects.create(**review)

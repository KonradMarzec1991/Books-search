"""
Module with general helper functions or classes
"""
import os
import csv
from functools import wraps

from .models import (
    Author,
    Book,
    Review
)


def upload_once(func):
    """
    This decorator checks if fixtures were uploaded to database
    as only one upload is permitted
    """
    already_uploaded = 'This fixture is already uploaded'
    allowed_files = ('books.csv', 'reviews.csv')

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper for uploading methods
        We do not need to check Author model separately, because we get
        all author data from books.csv fixture
        """
        csv_name = func.__name__.split('_')[-1]
        if csv_name not in allowed_files:
            raise IOError

        if csv_name == 'books' and Book.objects.exists():
            return already_uploaded
        if csv_name == 'reviews' and Review.objects.exists():
            return already_uploaded

        return func(*args, **kwargs)
    return wrapper


class FixtureCreator:
    """
    `FixtureCreator` uploads to db fixtures from csv files
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[-1]

    def csv_generator(self, delimiter=','):
        """
        Creates generator with csv data, omits headers
        :param delimiter: a sign, data in csv is partitioned off
        :return: generator
        """
        with open(self.path) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            next(reader, None)  # skip the headers

            for row in reader:
                yield row

    def console_response(self):
        """Returns appropriate console answer"""
        return f'Fixture {self.name} successfully uploaded to db'

    def upload(self):
        """
        Depending on self name,
        method decides which method should be run to create objects in db
        """
        if self.name == 'books.csv':
            return self.create_books()
        return self.create_reviews()

    @upload_once
    def create_books(self):
        """
        Creates objects for Author and Book models
        :return: console response
        """
        for row in self.csv_generator():
            isbn, title, author_name, genre = tuple(row)
            author, _ = Author.objects.get_or_create(name=author_name)

            Book.objects.create(
                isbn=isbn,
                title=title,
                author_id=author.id,
                genre=genre
            )
        return self.console_response()

    @upload_once
    def create_reviews(self):
        """
        Creates objects for Review model
        :return: console response
        """
        for row in self.csv_generator():
            isbn, rate, description = tuple(row)

            Review.objects.create(
                rate=int(rate),
                description=description,
                book_id=Book.objects.filter(isbn=isbn).first().id
            )
        return self.console_response()
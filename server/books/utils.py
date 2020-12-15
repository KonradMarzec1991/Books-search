"""
Module with general helper functions or classes
"""
import csv

from .models import (
    Author,
    Book,
    Review
)


class FixtureCreator:
    """
    `FixtureCreator` uploads to db fixtures from csv files
    """
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]

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

    def upload(self):
        """
        Depending on self name,
        method decides which method should be run to create objects in db
        """
        if self.name == 'books.csv':
            self.create_books()
        else:
            self.create_reviews()

    def create_books(self):
        """
        Creates objects for Author and Book models
        :return: None
        """
        for row in self.csv_generator():
            isbn, title, author_name, genre = tuple(row)
            author, created = Author.objects.get_or_create(name=author_name)

            Book.objects.create(
                isbn=isbn,
                title=title,
                author_id=author.id,
                genre=genre
            )

    def create_reviews(self):
        """
        Creates objects for Review model
        :return: None
        """
        for row in self.csv_generator():
            isbn, rate, description = tuple(row)

            Review.objects.create(
                rate=int(rate),
                description=description,
                book_id=Book.objects.filter(isbn=isbn).first().id
            )

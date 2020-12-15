"""
Django models module
"""
import operator
from functools import reduce

from django.db import models
from django.db.models import (
    Q,
    Avg,
    Count
)


class Author(models.Model):
    """
    Author model

    name - full name (first name and last name) of book author
    """
    name = models.CharField(max_length=100)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.name


class BookManager(models.Manager):
    """
    `BookManager` class contains methods for filtering books
    """

    # I know that theory says 3 parameters are max number, but for consistency
    # sake I decided to leave it as it is (for now)
    def filter_qs_by(self, q=None, isbn=None, genre=None, author=None):
        """Filters by single value or iterable"""
        qs = self.get_queryset()
        if q:
            qs = qs.filter(title__icontains=q)
        if isbn:
            qs = qs.filter(isbn=isbn)
        if author:
            qs = qs.filter(author__name__icontains=author)

        if genre:
            clauses = (Q(genre__icontains=gnr) for gnr in genre.split(','))
            query = reduce(operator.or_, clauses)
            qs = qs.filter(query)
        return qs

    @staticmethod
    def average_reviews(qs, rate_gte=None, rate_lte=None):
        """
        Aggregates books' review average rate and
        filters greater or/and lower than given values
        """
        if rate_gte:
            qs = qs.annotate(avg=Avg('reviews__rate')).filter(avg__gte=rate_gte)
        if rate_lte:
            qs = qs.annotate(avg=Avg('reviews__rate')).filter(avg__lte=rate_lte)
        return qs

    @staticmethod
    def count_reviews(qs, count_gte=None, count_lte=None):
        """
        Aggregates books' review count and
        filters greater or/and lower than given values
        """
        if count_gte:
            qs = qs.annotate(cnt=Count('reviews')).filter(cnt__gte=count_gte)
        if count_lte:
            qs = qs.annotate(cnt=Count('reviews')).filter(cnt__lte=count_lte)
        return qs


class Book(models.Model):
    """
    Book model

    isbn - unique book identifier
    title - book's title
    author - foreign key to Author model
    genre - choice field, depending on GENRES tuple
    """
    GENRES = (
        'Kryminał',
        'Dramat',
        'SciFi',
        'Sensacyjna',
        'Literatura młodzieżowa',
        'Literatura obyczajowa'
    )

    GENRE_CHOICES = tuple((item, item) for item in GENRES)

    isbn = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)

    objects = BookManager()

    class Meta:  # pylint: disable=too-few-public-methods
        ordering = ('title', )

    def __str__(self):
        return f'{self.title} ({self.isbn}) of {self.author.name}'


class Review(models.Model):
    """
    Review model

    rate - small integer value (in serializer it will
    be validate in range (1, 6))

    description - user's comment to book
    book - foreing key for Book model
    """
    rate = models.PositiveSmallIntegerField()
    description = models.TextField()
    book = models.ForeignKey(
        'Book',
        related_name='reviews',
        on_delete=models.CASCADE
    )

    @staticmethod
    def get_book_title(book_id):
        """
        Gets name of book for given review
        :param book_id: book identifier (database id, not isbn)
        :return: name of book
        """
        return Book.objects.filter(id=book_id).first().title

    def __str__(self):
        return f'Rate {self.rate} of {self.get_book_title(self.book_id)}'

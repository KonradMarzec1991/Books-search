from django.db import models


class Author(models.Model):
    """
    Author model

    name - full name (first name and last name) of book author
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

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

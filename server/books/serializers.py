# pylint: disable=too-few-public-methods
"""
Serializers module
"""
from rest_framework import serializers
from .models import Author, Book, Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    This serializer is used only as field in BookSerializer
    """
    class Meta:
        model = Review
        fields = ('rate', 'description')


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerialzier validates Book model and adds additional field

    author - name of author (default it is author_id)
    reviews = list of reviews with rating and description
    review_count - number of reviews
    rating - average of reviews' rates
    """
    author = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Author.objects.all()
    )

    reviews = ReviewSerializer(many=True)
    review_count = serializers.IntegerField(
        source='reviews.count',
        read_only=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'id', 'isbn', 'title', 'genre',
            'author', 'rating', 'review_count', 'reviews'
        )

    def get_rating(self, instance):
        """This method calculates average value for rates"""
        rate_sum, rate_count = 0, 0
        for rev in instance.reviews.all():
            rate_sum += rev.rate
            rate_count += 1
        return round(rate_sum / rate_count, 2) if rate_count else None

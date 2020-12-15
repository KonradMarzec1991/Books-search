"""
Views module
"""
from rest_framework import generics

from .models import Book
from .serializers import BookSerializer
from .pagination import BookPagination


class BookList(generics.ListAPIView):
    """
    BookList view allows to filter set of book objects
    """
    pagination_class = BookPagination

    def get_queryset(self):
        """Gets request parameters and filters queryset"""
        params = self.request.query_params

        q = params.get('q', None)
        isbn = params.get('isbn', None)
        author = params.get('author', None)
        genre = params.get('genre', None)

        qs = Book.objects.filter_qs_by(q, isbn, genre, author)

        rate_gte = params.get('rate_gte', None)
        rate_lte = params.get('rate_lte', None)
        rate_gte = float(rate_gte) if rate_gte else None
        rate_lte = float(rate_lte) if rate_lte else None

        qs = Book.objects.average_reviews(qs, rate_gte, rate_lte)

        count_gte = params.get('count_gte', None)
        count_lte = params.get('count_lte', None)
        count_gte = int(count_gte) if count_gte else None
        count_lte = int(count_lte) if count_lte else None

        qs = Book.objects.count_reviews(qs, count_gte, count_lte)
        return qs

    def list(self, request, *args, **kwargs):
        """Settings for book list"""
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class BookDetail(generics.RetrieveAPIView):
    """View for books retrieve"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'

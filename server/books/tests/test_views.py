import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.usefixtures('reviews')
class TestBookList:

    def test_list(self):
        response = APIClient().get(reverse('book-list'))
        queryset = response.data
        assert queryset['num_of_books'] == 2
        assert queryset['num_of_pages'] == 1
        assert len(queryset['books']) == 2

    def test_aggregation(self):
        response = APIClient().get(reverse('book-list'))
        queryset = response.data['books']
        assert queryset[0]['rating'] == 3.33
        assert queryset[0]['review_count'] == 3

    def test_q(self):
        response = APIClient().get('/books/?q=Ballada')
        queryset = response.data['books']
        assert len(queryset) == 1
        assert queryset[0]['title'] == 'Ballada ptaków i węży'

    def test_retrieve(self):
        response = APIClient().get(reverse('book-retrieve', args=[2]))
        book = response.data
        assert book['title'] == 'Osiedle RZNiW'
        assert book['review_count'] == 0

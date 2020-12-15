## Books-search
<hr >

### Introduction
Books-search is simple Django REST applications, which helps filter books.

### Installation
Please follow below steps:
1) `https://github.com/KonradMarzec1991/Books-search.git`
2) `docker-compose up --build`

Fixtures and migrations will be done automatically.

### Usage
In order to filter books, please use endpoint `/books/`.

There are several options you can use to filter (case-insensitive):
1) by `title`, example: `/books/?q=some_title`
2) by `genre`, example: `/books/?genre=one_genre,second_genre`
3) by `isbn`, example: `/books/?isbn=some_isbn`
4) by `author`, example: `/books/?author=some_author`

You can also filter by rating or review count:
1) by `rating`, example: `books/?rate_gte=2.5&rate_lte=4.5`
2) by `count`, example: `books/?count_lte=4`


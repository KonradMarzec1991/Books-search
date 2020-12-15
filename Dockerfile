FROM python:3.8

COPY ./requirements.txt /books/
COPY ./run.sh /books/

RUN apt-get update
RUN pip install -r /books/requirements.txt

COPY ./ /books/
WORKDIR /books

RUN chmod a+x /books/run.sh
CMD /books/run.sh
"""
Upload_file command module
"""
from django.core.management.base import BaseCommand
from books.utils import FixtureCreator
import os


class Command(BaseCommand):
    """
    This command helps to upload csv data to database
    """
    help = 'Upload objects (books, reviews) from csv file'

    def add_arguments(self, parser):
        """Gets file_name"""
        parser.add_argument(
            'file_name',
            type=str,
            help='The file that contains required to upload data'
        )

    def handle(self, *args, **kwargs):
        """
        Gets file name, gets file from /fixtures folder and using
        `FixtureCreator` uploads to database csv fixtures
        """
        file_name = kwargs.get('file_name', None)
        if file_name is None:
            raise ValueError('File_name cannot be None')

        path = f'{os.getcwd()}/fixtures/{file_name}.csv'
        try:
            console_response = FixtureCreator(path).upload()

            self.stdout.write(self.style.SUCCESS(console_response))
        except IOError:
            self.stdout.write(self.style.WARNING(
                f'Unable to read file {path} or file contains wrong data'
            ))

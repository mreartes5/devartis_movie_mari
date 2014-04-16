#! coding: utf-8
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from movies.models import Movie


RATINGS_FILENAME = "ratings.list.small"

START_PROCESSING_MOVIES_STRING = "MOVIE RATINGS REPORT\n"


class Command(BaseCommand):
    def create_or_update_movie_from_line(self, line):
        movie_parts_separator = "  "

        self.stdout.write(u'Processing line {line}'.format(line=line))

        movie_line_parts = filter(None, (line.split(movie_parts_separator)))

        title = movie_line_parts[3].split("\" (")[0][1:]
        year = movie_line_parts[3].split("\" (")[1][:-2]

        new_or_updated_movie = Movie()
        new_or_updated_movie.imdb_rank = float(movie_line_parts[2])
        new_or_updated_movie.title = title
        new_or_updated_movie.year = year
        new_or_updated_movie.imdb_votes = int(movie_line_parts[1])
        new_or_updated_movie.current_rating = new_or_updated_movie.imdb_rank
        new_or_updated_movie.total_votes = new_or_updated_movie.imdb_votes
        new_or_updated_movie.save()

        self.stdout.write(unicode(new_or_updated_movie))
        self.stdout.write('')

    def should_ommit_current_line(self, current_movie_description_string_line):
        return not ("{" in current_movie_description_string_line)

    def initialize_ratings_file_with_name(self, filename):
        self.stdout.write('Opening ratings ratings_file...')
        ratings_file = open(filename)

        current_movie_description_string_line = ''

        while current_movie_description_string_line != START_PROCESSING_MOVIES_STRING:
            current_movie_description_string_line = ratings_file.next()

        ratings_file.next()
        ratings_file.next()

        return ratings_file

    def handle(self, *args, **options):
        try:
            ratings_file = self.initialize_ratings_file_with_name(RATINGS_FILENAME)

            for current_movie_description_string_line in ratings_file:
                current_movie_description_string_line = current_movie_description_string_line.decode('utf-8')
                if self.should_stop_processing_ratings_file(current_movie_description_string_line):
                    break

                if self.should_ommit_current_line(current_movie_description_string_line):
                    self.create_or_update_movie_from_line(current_movie_description_string_line)

        except IOError:
            CommandError('Error processing ratings file.')

        finally:
            self.stdout.write('Closing ratings file...')
            ratings_file.close()

    def should_stop_processing_ratings_file(self, current_movie_description_string_line):
        return current_movie_description_string_line == '\n'

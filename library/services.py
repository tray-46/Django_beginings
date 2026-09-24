from django.db.models import Avg

from library.models import Book, BookReview


class BookServices:

    @staticmethod
    def calculate_average_rating(book_id):
        reviews = BookReview.objects.filter(book_id=book_id)

        if not reviews.exists():
            return None
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return average_rating

    @staticmethod
    def is_popular(book_id, threshold=4):
        average_rating = BookServices.calculate_average_rating(book_id)

        if average_rating is None:
            return False
        return average_rating >= threshold

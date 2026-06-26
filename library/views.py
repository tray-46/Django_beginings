from django.shortcuts import render
from library.models import Book


# Create your views here.
def books_list(request):
    books = Book.objects.order_by("author__first_name", "author__last_name", "title")
    return render(request, "library/books_list.html", {"books": books})


def book_details(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, "library/book_details.html", {"book": book})

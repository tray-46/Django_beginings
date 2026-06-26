from django.shortcuts import render
from library.models import Book


# Create your views here.
def books_list(request):
    books = Book.objects.all()
    return render(request, "books_list.html", {"books": books})


def book(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, "book_details.html", {"book": book})

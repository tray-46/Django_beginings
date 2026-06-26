from django.shortcuts import render
from library.models import Book, Author


# Create your views here.
def books_list(request):
    books = Book.objects.order_by("author__first_name", "author__last_name", "title")
    return render(request, "library/books_list.html", {"books": books})


def book_details(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, "library/book_details.html", {"book": book})


def index(request):
    return render(request, "library/index.html")


def authors_list(request):
    authors = Author.objects.order_by("first_name", "last_name")
    return render(request, "library/authors_list.html", {"authors": authors})


def author_details(request, pk):
    author = Author.objects.get(pk=pk)
    print(author)
    return render(request, "library/author_details.html", {"author": author})

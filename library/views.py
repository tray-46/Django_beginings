from http.client import responses

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from library.forms import ContactForm, CommentForm, BookForm, AuthorForm
from library.models import Book, Author, Article


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


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by("-created_at")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "author", "article_date", "content"]
    success_url = reverse_lazy("library:article_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data["error_message"] = "Please correct the errors below."
        return response
        # context = self.get_context_data(form=form)
        # context["error_message"] = "Please correct the errors below."
        # return self.render_to_response(context)


class ArticleDetailView(DetailView):
    model = Article

    @staticmethod
    def get_additional_data():
        return "Additional data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_data"] = self.get_additional_data()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_published:
            raise Http404("Статья не найдена")
        return obj


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "author", "content"]
    success_url = reverse_lazy("library:article_list")


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("library:article_list")


class BookListView(ListView):
    model = Book

    def get_queryset(self):
        return Book.objects.filter(publication_data__year__gt=1900)


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_more_book_count"] = self.object.author.books.count() - 1
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    # fields = ["author", "title", "publication_data", "cover_art", "description",]
    form_class = BookForm
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    # fields = ["author", "title", "publication_data", "cover_art", "description",]
    form_class = BookForm
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("library:book_list")


class ContactsFormView(FormView):
    template_name = "library/contacts_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("library:article_list")

    def form_valid(self, form: ContactForm):
        form.send_email()
        return super().form_valid(form)


class CommentFormView(FormView):
    template_name = "library/comment_form.html"
    form_class = CommentForm
    success_url = reverse_lazy("library:article_list")

    def form_valid(self, form: CommentForm):
        form.save()
        return super().form_valid(form)


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("library:authors_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("library:authors_list")

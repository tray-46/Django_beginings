from http.client import responses
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View

from library.forms import ContactForm, CommentForm, BookForm, AuthorForm, BookReviewForm
from library.models import Book, Author, Article, BookReview, BookRecommendation


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
    authors = cache.get("authors_list")
    if not authors:
        authors = Author.objects.order_by("first_name", "last_name")
        cache.set("authors_list", authors, 60 * 15)
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

@method_decorator(cache_page(60 * 15), name="dispatch")
class BookListView(ListView):
    model = Book

    def get_queryset(self):
        queryset = cache.get("book_list")
        if not queryset:
            queryset = Book.objects.filter(publication_data__year__gt=1900)
            cache.set("book_list", queryset)
        return queryset

@method_decorator(cache_page(60 * 15), name="dispatch")
class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_more_book_count"] = self.object.author.books.count() - 1
        context["recommended_by"] = self.object.book_recommendations.all().values_list("reviewer", flat=True)
        return context


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    # fields = ["author", "title", "publication_data", "cover_art", "description",]
    form_class = BookForm
    permission_required = "library.add_book"
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    # fields = ["author", "title", "publication_data", "cover_art", "description",]
    form_class = BookForm
    permission_required = "library.change_book"
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = "library.delete_book"
    success_url = reverse_lazy("library:book_list")


class BookReviewCreateView(LoginRequiredMixin, CreateView):
    model = BookReview
    form_class = BookReviewForm
    success_url = reverse_lazy("library:book_list")

    def form_valid(self, form):
        if not self.request.user.has_perm("library.can_review_book"):
            return HttpResponseForbidden("У Вас нет прав для рецензирования книги.")

        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        review = form.save(commit=False)
        review.book = book
        review.author = self.request.user
        return super().form_valid(form)


class BookRecommendationView(LoginRequiredMixin, View):

    def post(self, request, book_pk):
        if not self.request.user.has_perm("library.can_recommend_book"):
            return HttpResponseForbidden("У Вас нет прав для рекоммендации книги.")

        book = get_object_or_404(Book, pk=book_pk)
        BookRecommendation.objects.create(book=book, reviewer=request.user)
        return redirect("library:book_list")


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


class AuthorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("library:authors_list")


class AuthorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("library:authors_list")

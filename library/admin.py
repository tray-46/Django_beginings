from django.contrib import admin
from .models import Author, Book, BookReview


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "birth_date",)
    search_fields = ("last_name", "first_name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "publication_data",)
    list_filter = ("author",)
    search_fields = ("author__last_name", "author__first_name", "title",)

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book__title",)

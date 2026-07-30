from config import settings
from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"
        ordering = ["last_name", "first_name"]


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    publication_data = models.DateField(verbose_name="Дата публикации")
    cover_art = models.ImageField(upload_to="books/covers/", null=True, blank=True, verbose_name="Обложка")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "книги"
        ordering = ["title"]
        permissions = [("can_review_book", "Can review book"), ("can_recommend_book", "Can recommend book"), ]


class Article(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    content = models.TextField()
    article_date = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["title"]


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class BookReview(models.Model):
    RATING_CHOICES = [
        (1, "1 star"),
        (2, "2 star"),
        (3, "3 star"),
        (4, "4 star"),
        (5, "5 star"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_reviews", verbose_name="Книга")
    author = models.CharField(max_length=100, verbose_name="Автор")
    title = models.CharField(max_length=250, verbose_name="Заголовок", help_text="Введите заголовок для рецензии")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=0, verbose_name="Рейтинг книги",
                                              help_text="Оцените книгу")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "рецензия"
        verbose_name_plural = "рецензии"
        ordering = ["title", "created_at"]


class BookRecommendation(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_recommendations", verbose_name="Книга")
    reviewer = models.CharField(max_length=100, verbose_name="Рецензент")

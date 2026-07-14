from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"
        ordering = ["name"]

class Profile(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="profiles/images/", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
        ordering = ["name"]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"
        ordering = ["name"]

class Student(models.Model):
    FIRST_YEAR = "first"
    SECOND_YEAR = "second"
    THIRD_YEAR = "third"
    FOURTH_YEAR = "fourth"

    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, "Первый курс"),
        (SECOND_YEAR, "Второй курс"),
        (THIRD_YEAR, "Третий курс"),
        (FOURTH_YEAR, "Четвёртый курс"),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    email = models.EmailField()
    nickname = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(help_text="Введите возраст студента", verbose_name="Возраст")
    year = models.CharField(max_length=6, choices=YEAR_IN_SCHOOL_CHOICES, default=FIRST_YEAR, verbose_name="Курс")
    photo = models.ImageField(upload_to="students/photos/%Y", null=True, blank=True, verbose_name="Фотография")
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name="students", null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"
        ordering = ["last_name", "first_name"]

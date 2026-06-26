from django.core.management import BaseCommand, call_command, CommandError
from library.models import Author, Book


class Command(BaseCommand):

    help = "Add books to database"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        Author.objects.all().delete()

        try:
            call_command("loaddata", "library_fixture.json", database="library_db", app="library", format="json",
                         ignorenonexistent=True)
            self.stdout.write((self.style.SUCCESS(f"Successfully loaded books from fixture.")))
        except CommandError as e:
            self.stdout.write((self.style.ERROR(f"Error loading fixture: {e}")))

        author, _ = Author.objects.get_or_create(first_name="Антон", last_name="Чехов", birth_date="1860-01-29")

        books = [
            {"title": "Палата № 6", "publication_data": "1892-01-01", "author": author},
            {"title": "Три сестры", "publication_data": "1901-01-01", "author": author},
            {"title": "Вишнёвый сад", "publication_data": "1904-01-01", "author": author},
        ]

        for book in books:
            _, created = Book.objects.get_or_create(**book)
            if created:
                self.stdout.write((self.style.SUCCESS(f"Successfully created book: {book["title"]}")))
            else:
                self.stdout.write((self.style.WARNING(f"Book already exists: {book['title']}.")))

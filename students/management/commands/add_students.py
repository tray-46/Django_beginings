from django.core.management import BaseCommand, call_command, CommandError
from students.models import Student, Group


class Command(BaseCommand):
    help = "Add students to the database"

    def handle(self, *args, **options):

        Student.objects.all().delete()
        Group.objects.all().delete()

        try:
            call_command("loaddata", ".\students\\fixtures\groups_fixture.json", format="json", app="students",
                         database="students_db", ignorenonexistent=True)
            self.stdout.write((self.style.SUCCESS(f"Successfully loaded groups data from fixture")))
            call_command("loaddata", ".\students\\fixtures\students_fixture.json", format="json", app="students",
                         database="students_db", ignorenonexistent=True)
            self.stdout.write((self.style.SUCCESS(f"Successfully loaded students data from fixture")))
        except CommandError as e:
            self.stdout.write((self.style.ERROR(f"Error loading fixture: {e}")))

        group, _ = Group.objects.get_or_create(name="Группа 1")

        students = [
            {"first_name": "Иван", "last_name": "Иванов", "age": 18, "year": Student.FIRST_YEAR, "group": group},
            {"first_name": "Пётр", "last_name": "Петров", "age": 18, "year": Student.FIRST_YEAR, "group": group},
            {"first_name": "Сергей", "last_name": "Сергеев", "age": 18, "year": Student.FIRST_YEAR, "group": group},
        ]

        for student_data in students:
            student, created = Student.objects.get_or_create(**student_data)
            if created:
                self.stdout.write((self.style.SUCCESS(f"Successfully added student: "
                                                      f"{student_data['first_name']} {student_data['last_name']}")))
            else:
                self.stdout.write((self.style.WARNING(f"Student already exists: "
                                                      f"{student_data['first_name']} {student_data['last_name']}")))

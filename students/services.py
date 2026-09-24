from students.models import Student, Grade

class StudentService:

    @staticmethod
    def get_full_name(student_id):
        student = Student.objects.get(pk=student_id)
        return f"{student.first_name} {student.last_name}"

    @staticmethod
    def calculate_average_score(student_id):
        grades = Grade.objects.filter(student_id=student_id)
        if not grades.exists():
            return None
        total_score = sum(grade.score for grade in grades)
        average_score = total_score / grades.count()
        return average_score

    @staticmethod
    def has_passed(student_id, passing_score=60):
        average_grade = StudentService.calculate_average_score(student_id)
        if average_grade is None:
            return False
        return average_grade >= passing_score
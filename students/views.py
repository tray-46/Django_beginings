from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import StudentForm
from .models import Student

# Create your views here.
def example_view(request):
    # return HttpResponse("Welcome to example view.")
    return render(request, "students/example.html")


def show_data(request):
    if request.method == "GET":
        print(request.GET)
        # return HttpResponse("Welcome to show data view.")
        return render(request, "students/show_data.html")

def submit_data(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("Данные отправлены.")
    return HttpResponse("Здесь должна быть форма для данных.")

def show_item(request, item_id):
    print(item_id)
    # return HttpResponse(f"Welcome to show item_{item_id} view.")
    return render(request, "students/show_item.html", {"item_id": item_id})


def show_about(request):
    return render(request, "students/about.html")


def contact(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        message = request.POST.get("message")

        # tag = Tag(name=name)
        # tag.save()

        # Tag.objects.create(name=name)

        # tags = Tag.objects.all()
        # print(tags)
        # for tag in tags:
        #     print(f"{type(tag)} {tag.name}")
        # return HttpResponse(f"Спасибо {name}! Ваше сообщение получено.\ntags: {" ,".join(tags.values_list("name", flat=True))}")

        # students= Student.objects.filter(first_name__icontains=name)
        # print(students)

        # try:
        #     student = Student.objects.get(last_name=name)
        #     print(student)
        #     student.year = Student.SECOND_YEAR
        #     student.save()
        # except Student.DoesNotExist:
        #     print(f"Student {name} does not exist")

        # try:
        #     tag = Tag.objects.get(name=name)
        #     tag.delete()
        # except Tag.DoesNotExist:
        #     print(f"tag {name} does not exist")

        # students = Student.objects.exclude(year=Student.SECOND_YEAR)
        # print(students)

        students = Student.objects.all().order_by("age")
        print(students)
        return HttpResponse(f"Спасибо {name}! Ваше сообщение получено.")
    return render(request, "students/contact.html")


def example(request):
    return render(request, "students/example.html")


def index(request):
    student = Student.objects.get(id=1)
    # context = {
    #     "student_name": f"{student.first_name} {student.last_name}",
    #     "student_year": student.get_year_display(),
    # }
    context = {"student": student}
    if student.photo:
        print(student.photo.path)
        print(student.photo.url)
    return render(request, "students/index.html", context)


def students_list(request):
    students = Student.objects.all()
    return render(request, "students/student_list.html", {"students": students})


def student_details(request, pk):
    print(pk)
    student = Student.objects.get(pk=pk)
    print(student)
    return render(request, "students/student_details.html", {"student": student})


def home(request):
    return render(request, "students/home.html")


class StudentCreateView(CreateView):
    model = Student
    # fields = ["first_name", "middle_name", "last_name", "birth_date", "age", "year", "photo"]
    form_class = StudentForm
    success_url = reverse_lazy("students:students_list")


class StudentUpdateView(UpdateView):
    model = Student
    # fields = ["first_name", "middle_name", "last_name", "birth_date", "age", "year", "photo"
    form_class = StudentForm
    success_url = reverse_lazy("students:students_list")

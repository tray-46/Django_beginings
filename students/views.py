from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import StudentForm
from .models import Student
from .services import StudentService


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

@method_decorator(cache_page(60 * 15), name="dispatch")
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = "students"

    def get_queryset(self):
        if not self.request.user.has_perm("students.view_student"):
            return Student.objects.none()
        return Student.objects.all()


class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.object.id

        context["full_name"] = StudentService.get_full_name(student_id)
        context["average_grade"] = StudentService.calculate_average_score(student_id)
        context["has_passed"] = StudentService.has_passed(student_id)
        return context


class StudentCreateView(CreateView):
    model = Student
    # fields = ["first_name", "middle_name", "last_name", "birth_date", "age", "year", "photo"]
    form_class = StudentForm
    success_url = reverse_lazy("students:student_list")


class StudentUpdateView(UpdateView):
    model = Student
    # fields = ["first_name", "middle_name", "last_name", "birth_date", "age", "year", "photo"
    form_class = StudentForm
    success_url = reverse_lazy("students:student_list")


class PromoteStudentView(LoginRequiredMixin, View):

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)

        if not request.user.has_perm("students.can_promote_student"):
            return HttpResponseForbidden("У вас нет прав для перевода студента.")

        student.year = Student.next_year(student.year)
        student.save()

        return redirect("students:student_list")


class ExpelStudentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)

        if not request.user.has_perm("students.can_expel_student"):
            return HttpResponseForbidden("У вас нет прав для исключения студента.")

        student.delete()
        return redirect("students:student_list")


def cached_view_example(request):
    data = cache.get("some_key")

    if not data:
        print("redist calc")
        data = "some expensive computation"
        cache.set("some_key", data, 60 * 15)

    return HttpResponse(data)

from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.example_view, name="example_view"),
    path("show_data/", views.show_data, name="show_data"),
    path("submit_data/", views.submit_data, name="submit_data"),
    path("item/<int:item_id>/", views.show_item, name="show_item"),
    path("about/", views.show_about, name="show_about"),
    path("contact/", views.contact, name="contact"),

    path("example/", views.example, name="example"),
    path("index/", views.index, name="index"),

    path("students_list/", views.students_list, name="students_list"),
    path("student_details/<int:pk>/", views.student_details, name="student_details"),
    path("student_detail/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),

    path("home", views.home, name="home"),

    path("student/new/", views.StudentCreateView.as_view(), name="student_create"),
    path("student/<int:pk>/edit", views.StudentUpdateView.as_view(), name="student_edit"),

    path("student/list/", views.StudentListView.as_view(), name="student_list"),
    path("student/<int:pk>/promote/", views.PromoteStudentView.as_view(), name="student_promote"),
    path("student/<int:pk>/expel/", views.ExpelStudentView.as_view(), name="student_expel"),

    path("student/cache/", views.cached_view_example, name="cached_view"),
]

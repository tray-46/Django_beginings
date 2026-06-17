from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def example_view(request):
    # return HttpResponse("Welcome to example view.")
    return render(request, "app/example.html")


def show_data(request):
    if request.method == "GET":
        print(request.GET)
        # return HttpResponse("Welcome to show data view.")
        return render(request, "app/show_data.html")

def submit_data(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("Данные отправлены.")

def show_item(request, item_id):
    print(item_id)
    # return HttpResponse(f"Welcome to show item_{item_id} view.")
    return render(request, "app/show_item.html", {"item_id": item_id})


def show_about(request):
    return render(request, "students/about.html")


def contact(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо {name}! Ваше сообщение получено.")
    return render(request, "students/contact.html")
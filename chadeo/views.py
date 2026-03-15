from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "chadeo/index.html")

def create_user(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

    else :
        return render(request, "chadeo/create_user.html")

def login(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

    else :
        return render(request, "chadeo/login.html")
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@login_required(login_url="/chadeo/login")
def index(request):
    user = request.user
    
    return render(request, "chadeo/index.html",{"user": user})


def create_user(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        try:
            user = User.objects.get(username=username)
            print("user already exists")
            return redirect('chadeo:login_user') 
        except User.DoesNotExist:
            print("User not found")
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect('chadeo:login_user') 
    else :
        return render(request, "chadeo/create_user.html")

def login_user(request):
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('chadeo:index')
        else:
            return redirect('chadeo:login_user')

    else :
        return render(request, "chadeo/login.html")
    

def logout_user(request):
    logout(request)
    print("logout success")
    return redirect('chadeo:login_user')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import User_Detail

# Create your views here.
def homepage(request):
    return HttpResponse("Homepage")
    #return render(request, 'home.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            print(username)
        else:
            messages.error(request, "Invalid Employee ID or Password")
            return render(request, 'staff/login.html')
    return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST":
        print("Entered Post")
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                print("user exist")
                return render(request, 'signup.html')
                
            else:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                print("User saved")
                messages.success(request, "User created successfully")
                User_Detail.objects.create(
                    user=user,
                    name=request.POST['name'],
                    email=request.POST['email']
                )
                return render(request, 'login.html')
        else:
            messages.error(request, "Passwords do not match")
            print("Passwords do not match")
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('homepage')
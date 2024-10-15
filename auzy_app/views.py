from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
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
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('homepage')
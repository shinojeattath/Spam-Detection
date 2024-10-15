from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import User_Detail
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

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

def user_page(request):
    # if request.method == 'POST':
    #     url = request.POST['url']
    #     detect_spam(request, url)
    #     is_spam = request.session.get('is_spam')
    #     print(f'{url} is {is_spam}')
    return render(request, 'user_page.html')

def spamChat(request):
    return render(request, 'spam-chat.html')

################################
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": "Bearer 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"}
logger = logging.getLogger(__name__)
def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

@csrf_exempt
@require_http_methods(["POST"])
def detect_spam(request):
    try:
        # Parse JSON and extract the URL
        data = json.loads(request.body)
        url = data.get('url')
        print(data)
        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        # Query the model (replace with your actual query logic)
        output = query({"inputs": url})
        print(output)
        if output and isinstance(output, list) and len(output) > 0:
            result = output[0]
            if isinstance(result, list) and len(result) == 2:
                negative_score = next((item['score'] for item in result if item['label'] == 'NEGATIVE'), None)
                positive_score = next((item['score'] for item in result if item['label'] == 'POSITIVE'), None)
                
                if negative_score is not None and positive_score is not None:
                    is_spam = negative_score > positive_score 
                    request.session['is_spam'] = is_spam
                    print(negative_score)
                    return JsonResponse({
                        "url": url,
                        "is_spam": is_spam,
                        "negative_score": negative_score,
                        "positive_score": positive_score,
                        "model_output": output
                    })
                else:
                    return JsonResponse({"error": "Missing expected scores"}, status=500)
            else:
                return JsonResponse({"error": "Unexpected result structure"}, status=500)
        else:
            return JsonResponse({"error": "Unexpected model output"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.exception(f"Error processing URL {url}")
        return JsonResponse({"error": str(e)}, status=500)
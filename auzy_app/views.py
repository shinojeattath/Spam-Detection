from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import User_Detail, Message
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core import serializers

def homepage(request):
    return render(request, 'homepage.html')

def chat_rec(request):
    return render(request, 'chat-recv.html')

def check_spam(msg):
    try:
        # Example data to send
        data = {
            "url": msg
        }

        # Send the data to the spam detection endpoint
       

        # Check if the request was successful
        
        
        # POST request to detect_spam endpoint
        # response = requests.post("http://127.0.0.1:8000/detect_spam/", json=data)

        # Check if the request was successful
        # if response.status_code == 200:
        #     if response.is_spam:
        #         return True
        # else:
        #     return False

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def create_message(request):
    if request.method == "POST":
        content = request.POST.get('message')

        response = requests.post("http://127.0.0.1:8000/detect_spam/", json={
            'url': content
        })

        if response.status_code == 200:
            response_data = response.json()
            print(response_data['is_spam'])
            if response_data['is_spam']:
                spam = True
            else:
                spam = False

        message = Message.objects.create(
            content=content,
            is_spam = spam
        )
        # Respond with JSON
        return JsonResponse({
            'message': 'Message created successfully!',
            'id': message.id,
            'timestamp': message.timestamp,
        })

    # Render a simple form for testing purposes
    return render(request, 'create_message.html')

def fetch_messages(request):
    messages = Message.objects.filter(is_spam=False)
    
    # Serialize the queryset to JSON format
    messages_json = serializers.serialize('json', messages)
    
    # Return as a JSON response; the 'safe' parameter should be True
    return JsonResponse(messages_json, safe=False, json_dumps_params={'ensure_ascii': False})

def fetch_all_messages(request):
    messages = Message.objects.all()
    
    # Serialize the queryset to JSON format
    messages_json = serializers.serialize('json', messages)
    
    return JsonResponse(messages_json, safe=False)

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            print(username)
            return redirect('homepage')
        else:
            print("invalid password")
            print(username)
            messages.error(request, "Invalid Employee ID or Password")
            return render(request, 'login.html')
    return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST":
        print("Entered Post")
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        email = request.POST['email']
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                print("user exist")
                return render(request, 'signup.html')
                
            else:
                user = User.objects.create_user(username=username, password=pass1, email = email)
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
        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        # Query the model (replace with your actual query logic)
        output = query({"inputs": url})
        if output and isinstance(output, list) and len(output) > 0:
            result = output[0]
            if isinstance(result, list) and len(result) == 2:
                negative_score = next((item['score'] for item in result if item['label'] == 'NEGATIVE'), None)
                positive_score = next((item['score'] for item in result if item['label'] == 'POSITIVE'), None)
                
                if negative_score is not None and positive_score is not None:
                    is_spam = negative_score > positive_score 
                    request.session['is_spam'] = is_spam
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
from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('login/',views.user_login,name='user_login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'), 
    path('detect_spam/', views.detect_spam, name='detect_spam'),
    path('user_page/', views.user_page, name='user_page'),
    path('chat_rec/', views.chat_rec, name='chat_rec'),
    path('create_message/', views.create_message, name='create_message'),
    path('fetch_messages/', views.fetch_messages, name='fetch_messages'),
    path('fetch_all_messages/', views.fetch_all_messages, name='fetch_all_messages'),
    path('spam_chat/', views.spamChat, name='spam_chat'),

]
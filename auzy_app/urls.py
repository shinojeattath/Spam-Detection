from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('login/',views.user_login,name='user_login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'), 
]
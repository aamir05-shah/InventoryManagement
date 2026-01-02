from django.urls import path

from .views import Index , SignUpView , UC
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',  Index.as_view(), name="index"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name="logout"),

    path('uc/', UC.as_view() , name="uc"),
]
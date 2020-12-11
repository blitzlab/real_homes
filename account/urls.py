from django.urls import path, include
from . import views

app_name = "account"
urlpatterns = [
    path('', views.UserProfile.as_view(), name="account"),
    path('login', views.UserLoginView.as_view(), name="login"),
    path('logout', views.UserLogoutView.as_view(), name="logout"),
    path('signup', views.UserSignupView.as_view(), name="signup"),
]

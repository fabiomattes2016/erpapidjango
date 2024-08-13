from django.urls import path
from accounts.views.signin import Signin
from accounts.views.signup import Signup

urlpatterns = [
    path('signin', Signin.as_view()),
    path('signup', Signup.as_view()),
]
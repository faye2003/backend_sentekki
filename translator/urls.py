# translator/urls.py
from django.urls import path
from .views import translate_text
from .views import signup
from .views import login


urlpatterns = [
    path("translate/", translate_text, name="translate_text"),
    path("token/", login, name="login"),       # endpoint login
    path("register/", signup, name="signup"),  
]


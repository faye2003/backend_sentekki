# translator/urls.py
from django.urls import path
from .views import register, login, translate_text, add_correction

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path("translate/", translate_text, name="translate_text"),
    path("correction/", add_correction, name="add_correction"),
]


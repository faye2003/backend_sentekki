# translator/urls.py
from django.urls import path
from .views import register, login, translate_text, add_correction

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('translate/', translate_text, name='translate_text'),
    path('correction/<int:translator_id>/<int:sentence_index>/', add_correction, name='add_correction'),
]
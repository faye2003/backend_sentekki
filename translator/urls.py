# translator/urls.py
from django.urls import path
from .views import translate_text

urlpatterns = [
    path("translate/", translate_text, name="translate_text"),
    # path("correction/", views.add_correction, name="add_correction"),
]

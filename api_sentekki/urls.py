from django.contrib import admin
from django.urls import path, include
from translator import views  # 🔹 importe ton fichier views de l'app

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("translator.urls")),  # garde les URLs de l'app
    path("api/token/", views.login),           #la fonction login
    path("api/register/", views.signup),
]

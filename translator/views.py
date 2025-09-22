# translator/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from googletrans import Translator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@csrf_exempt
def translate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            dest = data.get("dest", "en")  # langue cible
            src = data.get("src", "auto")  # auto par défaut

            translator = Translator()
            result = translator.translate(text, src=src, dest=dest)

            return JsonResponse({
                "success": True,
                "translated_text": result.text,
                "src": result.src,
                "dest": result.dest
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)



@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Utilisateur existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user.save()
    return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Nom d’utilisateur ou mot de passe incorrect'}, status=400)

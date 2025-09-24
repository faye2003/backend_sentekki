# translator/views.py
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from googletrans import Translator as GoogleTranslator


@api_view(['POST'])
def translate_text(request):
    try:
        text = request.data.get("text", "")
        dest = request.data.get("dest", "en")  # langue cible
        src = request.data.get("src", "auto")  # auto par défaut

        if not text:
            return Response({"error": "Texte requis"}, status=status.HTTP_400_BAD_REQUEST)

        translator = GoogleTranslator()
        result = translator.translate(text, src=src, dest=dest)

        return Response({
            "success": True,
            "translated_text": result.text,
            "src": result.src,
            "dest": result.dest
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Nom d’utilisateur et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Utilisateur existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Nom d’utilisateur et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Nom d’utilisateur ou mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)

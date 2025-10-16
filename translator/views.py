from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from googletrans import Translator as GoogleTranslator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Language, Translator, CorrectionTranslator
from .serializers import TranslatorSerializer, CorrectionTranslatorSerializer
import re

def split_into_sentences(text):
    # Découpe après ., ! ou ? suivis d'espace(s) ou retour à la ligne
    sentences = re.split(r'(?<=[.!?])', text.strip())
    return [s.strip() for s in sentences if s.strip()]


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({
        "success": True,
        "user_id": user.id,
        "username": user.username
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    from django.contrib.auth import authenticate

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.username
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# --- Endpoint 1 : Traduction complète ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_text(request):
    """
    Traduit un texte et enregistre le résultat complet + phrases JSON
    """
    user = request.user
    input_text = request.data.get("input_text")
    lang_src = request.data.get("lang_src", "auto")
    lang_dest = request.data.get("lang_dest", "en")

    if not input_text:
        return Response({"error": "Le champ 'text' est requis."}, status=400)

    try:
        translator = GoogleTranslator()
        translated = translator.translate(input_text, src=lang_src, dest=lang_dest)
    except Exception as e:
        return Response({"error": f"Erreur de traduction : {str(e)}"}, status=500)

    src_lang, _ = Language.objects.get_or_create(code=translated.src, defaults={"name": translated.src})
    dest_lang, _ = Language.objects.get_or_create(code=lang_dest, defaults={"name": lang_dest})

    input_sentences = split_into_sentences(input_text)
    output_sentences = split_into_sentences(translated.text)

    input_json = [{"text": s} for s in input_sentences]
    output_json = [{"text": s} for s in output_sentences]

    trans = Translator.objects.create(
        user=user,
        lang_src=src_lang,
        lang_dest=dest_lang,
        input_text=input_text,
        output_text=translated.text,
        input_sentence=input_json,
        output_sentence=output_json,
    )

    serializer = TranslatorSerializer(trans)
    return Response(serializer.data, status=201)


# --- Endpoint 2 : Correction d'une phrase ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_correction(request):
    """
    Ajoute une correction à partir d'une phrase source et corrigée
    """
    user = request.user
    translator_id = request.data.get("translator_id")
    phrase_source = request.data.get("phrase_source")
    phrase_corrigee = request.data.get("phrase_corrigee")

    if not all([translator_id, phrase_source, phrase_corrigee]):
        return Response({"error": "translator_id, phrase_source et phrase_corrigee sont requis."}, status=400)

    try:
        translator = Translator.objects.get(pk=translator_id)
    except Translator.DoesNotExist:
        return Response({"error": "Traduction introuvable."}, status=404)

    correction = CorrectionTranslator.objects.create(
        translator=translator,
        user=user,
        phrase_source=phrase_source,
        phrase_corrigee=phrase_corrigee
    )

    serializer = CorrectionTranslatorSerializer(correction)
    return Response(serializer.data, status=201)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
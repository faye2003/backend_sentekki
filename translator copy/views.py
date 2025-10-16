from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from googletrans import Translator as GoogleTranslator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Language, Translator, CorrectionTranslator
from .serializers import TranslatorSerializer

# Fonction utilitaire pour découper en phrases
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_text(request):
    """
    Traduit un texte et enregistre le tout dans Translator
    (incluant les phrases sous forme JSON)
    """
    user = request.user
    input_text = request.data.get("text")
    lang_src = request.data.get("lang_src", "auto")
    lang_dest = request.data.get("lang_dest", "en")

    if not input_text:
        return Response({"error": "input_text requis"}, status=400)

    # Traduction Google
    translator = GoogleTranslator()
    translated = translator.translate(input_text, src=lang_src, dest=lang_dest)

    # Gestion des langues
    src_lang, _ = Language.objects.get_or_create(code=translated.src, defaults={"name": translated.src})
    dest_lang, _ = Language.objects.get_or_create(code=lang_dest, defaults={"name": lang_dest})

    # Découper les phrases
    input_sentences = split_into_sentences(input_text)
    output_sentences = split_into_sentences(translated.text)
    sentence_pairs = [
        {"index": i + 1, "src": src, "translated": out}
        for i, (src, out) in enumerate(zip(input_sentences, output_sentences))
    ]

    # Sauvegarder dans Translator (fusionné)
    translator_obj = Translator.objects.create(
        user=user,
        lang_src=src_lang,
        lang_dest=dest_lang,
        input_text=input_text,
        output_text=translated.text,
        sentence_count=len(sentence_pairs),
        sentences_data=sentence_pairs
    )

    serializer = TranslatorSerializer(translator_obj)
    return Response(serializer.data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_correction(request, translator_id, sentence_index):
    """
    Ajoute une correction sur une phrase spécifique
    """
    user = request.user
    corrected_text = request.data.get("corrected_text")

    if not corrected_text:
        return Response({"error": "Texte corrigé manquant"}, status=400)

    try:
        translator = Translator.objects.get(pk=translator_id)
    except Translator.DoesNotExist:
        return Response({"error": "Traduction introuvable"}, status=404)

    # Vérifier que la phrase existe
    sentences = translator.sentences_data
    if sentence_index < 1 or sentence_index > len(sentences):
        return Response({"error": "Index de phrase invalide"}, status=400)

    # Mettre à jour localement la phrase
    sentences[sentence_index - 1]['translated'] = corrected_text
    translator.sentences_data = sentences
    translator.output_text = " ".join([s['translated'] for s in sentences])
    translator.save()

    # Créer la correction
    CorrectionTranslator.objects.create(
        translator=translator,
        user=user,
        sentence_index=sentence_index,
        corrected_text=corrected_text
    )

    return Response({
        "message": "Correction enregistrée avec succès",
        "translator_id": translator.id,
        "sentence_index": sentence_index,
        "corrected_text": corrected_text
    }, status=200)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# translator/views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from googletrans import Translator

# @csrf_exempt
# def translate_text(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             text = data.get("text", "")
#             dest = data.get("dest", "en")
#             src = data.get("src", "auto")

#             translator = Translator()
#             result = translator.translate(text, src=src, dest=dest)

#             return JsonResponse({
#                 "success": True,
#                 "translated_text": result.text,
#                 "src": result.src,
#                 "dest": result.dest
#             })
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)}, status=400)
#     return JsonResponse({"error": "POST request required"}, status=405)
# python manage.py startapp translator

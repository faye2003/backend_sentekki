from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from googletrans import Translator as GoogleTranslator
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Translator, TranslateText, CorrectionTranslator, Language
from .serializers import TranslatorSerializer, CorrectionTranslatorSerializer

# Fonction utilitaire pour découper en phrases
import re

def split_into_sentences(text):
    # Découpe après ., ! ou ? suivis d'espace(s) ou retour à la ligne
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def translate_text(request):
    """
    Traduit un texte et enregistre la traduction + phrases
    """
    user = request.user
    input_text = request.data.get("text")
    lang_src = request.data.get("lang_src", "auto")
    lang_dest = request.data.get("lang_dest", "en")

    if not input_text:
        return Response({"error": "input_text requis"}, status=400)

    # Traduction avec Google
    translator = GoogleTranslator()
    translated = translator.translate(input_text, src=lang_src, dest=lang_dest)

    # Sauvegarde dans la DB
    src_lang, _ = Language.objects.get_or_create(code=translated.src, defaults={"name": translated.src})
    dest_lang, _ = Language.objects.get_or_create(code=lang_dest, defaults={"name": lang_dest})

    trans = Translator.objects.create(
        user=user,
        lang_src=src_lang,
        lang_dest=dest_lang,
        input_text=input_text,
        output_text=translated.text
    )

    # Découpage en phrases
    input_sentences = split_into_sentences(input_text)
    output_sentences = split_into_sentences(translated.text)

    for i, (src, out) in enumerate(zip(input_sentences, output_sentences), start=1):
        TranslateText.objects.create(
            translator=trans,
            sentence_number=i,
            sentence_src=src,
            sentence_translated=out
        )

    serializer = TranslatorSerializer(trans)
    return Response(serializer.data, status=201)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_correction(request, sentence_id):
    """
    Ajoute une correction sur une phrase traduite
    """
    try:
        sentence = TranslateText.objects.get(pk=sentence_id)
    except TranslateText.DoesNotExist:
        return Response({"error": "Phrase introuvable"}, status=404)

    correction_text = request.data.get("correction_text")
    if not correction_text:
        return Response({"error": "correction_text requis"}, status=400)

    correction = CorrectionTranslator.objects.create(
        sentence=sentence,
        user=request.user,
        correction_text=correction_text
    )

    serializer = CorrectionTranslatorSerializer(correction)
    return Response(serializer.data, status=201)



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

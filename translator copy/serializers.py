from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Translator, CorrectionTranslator, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TranslatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    lang_src = LanguageSerializer(read_only=True)
    lang_dest = LanguageSerializer(read_only=True)

    class Meta:
        model = Translator
        fields = [
            'id',
            'user',
            'lang_src',
            'lang_dest',
            'input_text',
            'output_text',
            'sentence_count',
            'sentences_data',  # le JSON avec toutes les phrases
            'created_at'
        ]


class CorrectionTranslatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    translator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorrectionTranslator
        fields = [
            'id',
            'translator',
            'user',
            'sentence_index',
            'corrected_text',
            'created_at'
        ]

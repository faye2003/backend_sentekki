from rest_framework import serializers
from .models import Translator, TranslateText, CorrectionTranslator, Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class TranslateTextSerializer(serializers.ModelSerializer):
    corrections = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TranslateText
        fields = ["id", "sentence_number", "sentence_src", "sentence_translated", "corrections"]


class TranslatorSerializer(serializers.ModelSerializer):
    sentences = TranslateTextSerializer(many=True, read_only=True)

    class Meta:
        model = Translator
        fields = ["id", "user", "lang_src", "lang_dest", "input_text", "output_text", "created_at", "sentences"]



class CorrectionTranslatorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CorrectionTranslator
        fields = ["id", "sentence", "user", "correction_text", "created_at"]


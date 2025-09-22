from rest_framework import serializers
from translator.models import Translator
from serializers.sentence_translator_serialiser import TranslateTextSerializer

class TranslatorSerializer(serializers.ModelSerializer):
    sentences = TranslateTextSerializer(many=True, read_only=True)

    class Meta:
        model = Translator
        fields = ["id", "user", "lang_src", "lang_dest", "input_text", "output_text", "created_at", "sentences"]
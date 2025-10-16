from rest_framework import serializers
from translator.models import TranslateText


class TranslateTextSerializer(serializers.ModelSerializer):
    corrections = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TranslateText
        fields = ["id", "sentence_number", "sentence_src", "sentence_translated", "corrections"]

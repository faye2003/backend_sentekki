from rest_framework import serializers
from translator.models import CorrectionTranslator

class CorrectionTranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrectionTranslator
        fields = ["id", "translator", "sentence", "user", "corrected_text", "created_at"]

from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 'en', 'fr', 'wo'
    name = models.CharField(max_length=100)  # English, Français, Wolof...

    def __str__(self):
        return f"{self.name} ({self.code})"


class Translator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_src = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translations_src")
    lang_dest = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translations_dest")
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.lang_src.code} -> {self.lang_dest.code}"


class TranslateText(models.Model):
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, related_name="sentences")
    sentence_number = models.IntegerField()
    sentence_src = models.TextField()
    sentence_translated = models.TextField()

    def __str__(self):
        return f"Sentence {self.sentence_number} ({self.translator.id})"


class CorrectionTranslator(models.Model):
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, related_name="corrections")
    sentence = models.ForeignKey(TranslateText, on_delete=models.CASCADE, related_name="corrections")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corrected_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction {self.id} by {self.user.username}"

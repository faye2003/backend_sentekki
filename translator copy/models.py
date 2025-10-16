from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Translator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_src = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translations_src")
    lang_dest = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="translations_dest")
    input_text = models.TextField()
    output_text = models.TextField()
    sentence_count = models.IntegerField(default=0)
    sentences_data = models.JSONField(default=list)  # stockage des phrases en JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.lang_src.code} -> {self.lang_dest.code}"


class CorrectionTranslator(models.Model):
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, related_name="corrections")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence_index = models.IntegerField(default=0)
    corrected_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction phrase {self.sentence_index} par {self.user.username}"

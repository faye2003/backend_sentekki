from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # ex: 'en', 'fr', 'wo'
    name = models.CharField(max_length=100)  # ex: 'English', 'Français'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Translator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='translations')
    lang_src = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translations_src')
    lang_dest = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translations_dest')

    # Texte complet
    input_text = models.TextField()
    output_text = models.TextField()

    # Nouvelles colonnes JSON
    input_sentence = models.JSONField(default=list)   # liste d’objets ou de phrases sources
    output_sentence = models.JSONField(default=list)  # liste d’objets ou de phrases traduites

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} | {self.lang_src.code} → {self.lang_dest.code}"


class CorrectionTranslator(models.Model):
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, related_name='corrections')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='corrections')

    phrase_source = models.TextField()
    phrase_corrigee = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Correction by {self.user.username} on {self.translator.id}"

from django.contrib import admin
from .models import Language, Translator, TranslateText, CorrectionTranslator

# Admin pour Language
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


# Admin pour Translator
@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang_src', 'lang_dest', 'input_text', 'output_text', 'created_at')
    search_fields = ('input_text', 'output_text', 'user__username')
    list_filter = ('lang_src', 'lang_dest', 'created_at')


# Admin pour TranslateText
@admin.register(TranslateText)
class TranslateTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'translator', 'sentence_number', 'sentence_src', 'sentence_translated')
    search_fields = ('sentence_src', 'sentence_translated', 'translator__user__username')
    list_filter = ('translator__lang_src', 'translator__lang_dest')


# Admin pour CorrectionTranslator
@admin.register(CorrectionTranslator)
class CorrectionTranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'translator', 'sentence', 'user', 'corrected_text', 'created_at')
    search_fields = ('corrected_text', 'translator__user__username', 'sentence__sentence_src')
    list_filter = ('translator__lang_src', 'translator__lang_dest', 'created_at')

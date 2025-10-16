from django.contrib import admin
from .models import Language, Translator, CorrectionTranslator


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang_src', 'lang_dest', 'created_at')
    search_fields = ('user__username', 'input_text', 'output_text')
    list_filter = ('lang_src', 'lang_dest', 'created_at')


@admin.register(CorrectionTranslator)
class CorrectionTranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'translator', 'user', 'phrase_source', 'phrase_corrigee', 'created_at')
    search_fields = ('phrase_source', 'phrase_corrige', 'translator__user__username')
    list_filter = ('created_at',)

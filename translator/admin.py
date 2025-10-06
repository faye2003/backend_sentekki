from django.contrib import admin
from .models import Language, Translator, CorrectionTranslator


# 🔤 Admin pour Language
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


# 🌍 Admin pour Translator
@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang_src', 'lang_dest', 'input_text', 'output_text', 'created_at')
    search_fields = ('input_text', 'output_text', 'user__username')
    list_filter = ('lang_src', 'lang_dest', 'created_at')

    readonly_fields = ('created_at',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('user', 'lang_src', 'lang_dest', 'created_at')
        }),
        ('Contenu', {
            'fields': ('input_text', 'output_text')
        }),
    )


# ✏️ Admin pour CorrectionTranslator
@admin.register(CorrectionTranslator)
class CorrectionTranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'translator', 'user', 'corrected_text', 'created_at')
    search_fields = ('corrected_text', 'translator__user__username')
    list_filter = ('translator__lang_src', 'translator__lang_dest', 'created_at')

    readonly_fields = ('created_at',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('translator', 'user', 'created_at')
        }),
        ('Correction', {
            'fields': ('corrected_text',)
        }),
    )

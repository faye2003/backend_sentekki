# translator/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from googletrans import Translator

@csrf_exempt
def translate_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            dest = data.get("dest", "en")  # langue cible
            src = data.get("src", "auto")  # auto par défaut

            translator = Translator()
            result = translator.translate(text, src=src, dest=dest)

            return JsonResponse({
                "success": True,
                "translated_text": result.text,
                "src": result.src,
                "dest": result.dest
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)
# python manage.py startapp translator

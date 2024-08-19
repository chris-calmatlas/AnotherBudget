from django.http import JsonResponse

def genericJsonError():
    return JsonResponse({"error": "true"})
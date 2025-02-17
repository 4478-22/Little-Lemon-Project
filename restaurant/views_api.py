from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        url = "http://yourdomain.com/api/auth/token/login/"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, data=data)

        return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({"error": "Invalid method"}, status=405)
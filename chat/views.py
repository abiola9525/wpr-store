# chat/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import ChatBot
# from .chatbot import get_response

def index(request):
    return render(request, 'chat.html')

chatbot = ChatBot()

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        response = chatbot.get_response(message)
        return JsonResponse({'answer': response})

    return JsonResponse({'error': 'Invalid request'}, status=400)

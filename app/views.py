from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from .tg_def import message_get
from .tg_def import text_send
from .tg_def import file_send
import json

class WebhookView(APIView):
    def post(self, request):
        message = message_get(request)
        if message["data"]["callback"] != "none":
            pass
        elif message["content"]["photo_id"] != "none":
            photo_get(message)
        elif message["content"]["audio"] != "none":
            pass
        elif message["content"]["document"] != "none":
            pass
        elif message["content"]["text"] != "none":
            text_get(message)
            chat_id = message["data"]["chat_id"]
            file_id = "AgACAgIAAxkBAAN7ZJ1qKAuGPXcpKpf2ZKcQx6KH7bcAAkPPMRtrNPBISezWDHZzYRQBAAMCAANzAAMvBA"
            file_send(file_id, chat_id)
        return HttpResponse()

def text_get(request):
    print(request)
    text_send(request)
    return 

def callback_get(request):
    print(request)
    return 

def photo_get(request):
    print(request)
    return 

def audio_get(request):
    print(request)
    return 

def document_get(request):
    print(request)
    return 
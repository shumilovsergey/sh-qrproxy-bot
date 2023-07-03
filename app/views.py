from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from .tg_def import message_get
from .tg_def import inline
from .serializers import ChatSerializer
import json

class WebhookView(APIView):
    def post(self, request):
        message = message_get(request)
        print(message)

        if message["content"]["text"] == "/start":
            chat_id = message["data"]["chat_id"]
            chat = {'chat_id' : chat_id }
            serializer = ChatSerializer(data=chat)
            if serializer.is_valid():
                serializer.save()
                keyboard = {
                    "inline_keyboard" : [
                        [
                            {'text': 'Создать', 'callback_data': 'rout_create'}
                        ],
                        [
                            {'text': 'Обратная связь', 'callback_data': 'contact'}
                        ]
                    ]
                }
            else:
                keyboard = {
                    "inline_keyboard" :  [
                        [
                            {'text': 'Редактировать', 'callback_data': 'rout_put'}
                        ],        
                        [
                            {'text': 'Показать', 'callback_data': 'rout_get'}
                        ], 
                        [
                            {'text': 'Обратная связь', 'callback_data': 'contact'}
                        ]                
                    ]
                } 
            text = "Меню:"
            
            inline(chat_id=chat_id, text=text, keyboard=keyboard)

        else:
            pass
        return HttpResponse()


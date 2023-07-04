from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from .tg_def import message_get
from .tg_def import message_send
from .tg_def import message_edit
from .tg_def import message_delete
from .serializers import ChatSerializer
from .models import Chats
import json
import requests

class WebhookView(APIView):
    def post(self, request):
        message = message_get(request)
        print(message)
        chat_id = message["data"]["chat_id"]
        message_id = message["data"]["message_id"]
        text = message["content"]["text"]
        callback = message["data"]["callback"]

        if text == "/start":
            start(message)

        elif callback == "rout_create":
            text = "Отправьте мне ссылку на ваш сайт"
            response = {
                "chat_id" : chat_id,
                "text" : text,
                "keyboard" : "none",
                "message_id" : message_id
            }
            message_edit(response)

###___CALLBACK___###
        else:
            user = Chats.objects.get(chat_id=chat_id)

            if user.last_callback == "rout_create":
                rout_create(message, user)

############
            elif user.last_callback == "none":
                message_delete(chat_id, message_id)

        return HttpResponse()



def start(message):
    chat_id = message["data"]["chat_id"]
    chat = {'chat_id' : chat_id }
    serializer = ChatSerializer(data=chat)
    if serializer.is_valid():
        serializer.save()

    user = Chats.objects.get(chat_id=chat_id)
    user.last_callback = "none"
    user.save()

    if user.privat_url == "none":
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
                    {'text': 'Редактировать', 'callback_data': 'rout_create'}
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
    message = {
        "chat_id" : chat_id,
        "text" : text,
        "keyboard" : keyboard
    }
    message_send(message)
    return 

def rout_create(message, user):
    chat_id = message["data"]["chat_id"]
    message_id = message["data"]["message_id"]

    url = message["content"]["text"]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = 200
        else:
            response = 400
    except:
        response = 400

    if response != 200:
        message_delete(chat_id, message_id)
        
        




    # try:
    #     response = url_check(url)
    # except:
    #     response = 400

    # if response == 200:
    #     user.last_callback = "none"
    #     user.privat_url = url
    #     user.save()



    return response
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
from .tg_def import qr_create
from .tg_def import photo_send
from .serializers import ChatSerializer
from .models import Chats
import json
import requests
from project.const import DOMAIN_NAME


MENU_BUTTON = {
        "inline_keyboard" :  [
            [
                {'text': 'Меню', 'callback_data': 'menu'}
            ]
        ]
    }


class WebhookView(APIView):
    def post(self, request):
        message = message_get(request)
        print(message)
        chat_id = message["data"]["chat_id"]
        message_id = message["data"]["message_id"]
        text = message["content"]["text"]
        callback = message["data"]["callback"]
        keyboard = "none"

        if text == "/start":
            start(message)

        elif callback == "rout_create":
            text = "Отправьте мне ссылку на ваш сайт"
            message_edit(chat_id, message_id, text, keyboard)
        
        elif callback == "menu":
            message_delete(chat_id, message_id)
            start(message)

        elif callback == "rout_get":
            message_delete(chat_id, message_id)
            user = Chats.objects.get(chat_id=chat_id)
            photo_id = user.qr_id
            text = "Вот ваш QrCode"
            keyboard = MENU_BUTTON
            photo_send(chat_id, text, keyboard, photo_id)
        
        elif callback == "contact":
            message_delete(chat_id, message_id)
            text = "Отзывы и предложения можно отправить по адресу wumilovsergey@gmail.com, либо в телеграме @sergey_showmelove!"
            keyboard = MENU_BUTTON
            message_send(chat_id, text, keyboard)
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
    user.public_url = f"{DOMAIN_NAME}/api/telegram_bot/{chat_id}"
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

    text = "Меню"

    message_send(chat_id, text, keyboard)
    return 

def rout_create(message, user):
    privat_url = message["content"]["text"]
    chat_id = message["data"]["chat_id"]
    message_id = message["data"]["message_id"]
    keyboard = "none"

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

        text = "Плохая ссылка, попробуйте еще раз!"
        message_id = user.last_id
        message_edit(chat_id, message_id, text, keyboard)
    else:
        message_delete(chat_id, message_id)
        message_id = user.last_id
        message_delete(chat_id, message_id)
        photo_id = qr_create(chat_id, user)

        user.privat_url = privat_url
        user.last_callback = "none"
        user.last_id = "none"
        user.save()

    return

class RedirectTelegramView(APIView):
    def get(self, request, chat_id):

        user = Chats.objects.get(chat_id=chat_id)
        if user.privat_url == "none":
            response = "none"
        else:
            response=redirect(user.privat_url)
        return response
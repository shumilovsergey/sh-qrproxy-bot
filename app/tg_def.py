import json
import requests
from project.const import BOT_TOKEN
from .models import Chats

def message_get(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'callback_query' in data:
        callback = data['callback_query']['data']
        message_id = data['callback_query']["message"]["message_id"]
        chat_id = data['callback_query']['from']["id"]
        user = Chats.objects.get(chat_id=chat_id)
        user.last_callback = callback
        user.save()      
    else:
        chat_id = data["message"]["chat"]["id"]
        message_id = data["message"]["message_id"]
        callback = "none"

    ###
    try: 
        text = data["message"]["text"]
    except:
        text = "none"
    ###    
    try:
        photo_id = data["message"]["photo"][0]["file_id"]
    except:
        photo_id = "none"
    ###
    try: 
        audio_name = data["message"]["audio"]["file_name"]
        audio_type = data["message"]["audio"]["mime_type"]
        audio_id = data["message"]["audio"]["file_id"]
        audio = {
            "audio_name" : audio_name,
            "audio_type" : audio_type,
            "audio_id" : audio_id
        }
    except:
        audio = "none"
    ###
    try:
        document_name = data["message"]["document"]["file_name"]
        document_type = data["message"]["document"]["mime_type"]
        document_id = data["message"]["document"]["file_id"]
        document = {
            "document_name" : document_name,
            "document_type" : document_type,
            "document_id" : document_id
        }
    except:
        document = "none"
    ###
    message = {
        "data" : {
            "chat_id" : chat_id,
            "message_id" : message_id,
            "callback" : callback
        }, 
        "content" : {
            "text" : text,
            "photo_id" : photo_id,
            "audio" : audio,
            "document" : document
        }
    }
    return message

def message_send(request):
    if request["keyboard"] == "none":
        data = { 
            "chat_id": request["chat_id"],
            "text": request["text"]
        }
    else:
        data = { 
            "chat_id": request["chat_id"],
            "text": request["text"],
            "reply_markup" : json.dumps(request["keyboard"])
        }

    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data)
    return response

def message_edit(request):
    if request["keyboard"] == "none":
        data = { 
            "chat_id": request["chat_id"],
            "text": request["text"],
            "message_id" : request["message_id"]
        }
    else:
        data = { 
            "chat_id": request["chat_id"],
            "text": request["text"],
            "message_id" : request["message_id"],
            "reply_markup" : json.dumps(request["keyboard"])
        }

    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", data)
    return response

def message_delete(chat_id, message_id):
    data = {
        "chat_id": chat_id,
        "message_id" : message_id
    }
    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage", data)
    return response





# def file_send(photo_id, chat_id):
#     bot_token = BOT_TOKEN

#     # Constructing the file download URL using the file_id
#     file_url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={photo_id}'

#     # Fetching the file path using the file_id
#     response = requests.get(file_url)
#     file_path = response.json()['result']['file_path']

#     # Constructing the file download URL
#     download_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'

#     # Sending the file to the specified chat
#     file_data = requests.get(download_url).content

#     url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
#     payload = {'chat_id': chat_id, 'photo': photo_id}


#     response = requests.post(url, data=payload)
#     print(response.json())   


#     return response
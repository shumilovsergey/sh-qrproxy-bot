from django.urls import path
from .views import WebhookView
from .views import RedirectTelegramView


urlpatterns = [
    path('', WebhookView.as_view(), name='webhook'),
    path('api/telegram_bot/<int:chat_id>/', RedirectTelegramView.as_view(), name='redirect'),
]
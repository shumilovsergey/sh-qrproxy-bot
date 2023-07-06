from django.urls import path
from .views import WebhookView
from .views import RedirectView


urlpatterns = [
    path('', WebhookView.as_view(), name='webhook'),
    path('api/telegram_bot/<int:chat_id>/', RedirectView.as_view(), name='redirect'),
]
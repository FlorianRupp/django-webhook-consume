from django_webhook_consume import views

from django.urls import path


urlpatterns = [
    path("github/<str:hook_id>", views.consume_web_hook)
]
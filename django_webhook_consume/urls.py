from django_webhook_consume import views

from django.urls import path


urlpatterns = [
    path("github/", views.consume_web_hook)
]
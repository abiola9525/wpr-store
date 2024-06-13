from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.index, name='index'),
    path('get-response/', views.get_response, name='get-response'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('chattxt/',views.chattxt), #chattxt - chat text to text
    path('chatstt/',views.chatstt), #chatstt
]

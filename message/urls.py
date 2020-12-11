from django.urls import path, include
from . import views

app_name = "message"
urlpatterns = [
    path('incoming-messages', views.MyMessages.as_view(), name="my_messages"),
    path('<pk>/<str:conversation_id>', views.message_detail, name="messsage_detail"),
]

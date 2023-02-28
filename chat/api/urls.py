from django.urls import path

from chat.api.views import ThreadDeleteCreateApiView, ThreadListApiView, MessageListCreateApiView, \
    MessageIsReadCreateApiView, UnreadMessageNumberListApiView

urlpatterns = [
    path('thread/', ThreadDeleteCreateApiView.as_view(), name='thread_create_delete'),
    path('thread_list/', ThreadListApiView.as_view(), name='thread_list'),
    path('message/', MessageListCreateApiView.as_view(), name='message_list_create'),
    path('message_isread/', MessageIsReadCreateApiView.as_view(), name='message_isread_create'),
    path('unread_messages/<int:id>/', UnreadMessageNumberListApiView.as_view(), name='unread_messages'),
]

from django.contrib.auth import get_user_model
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from chat.api.serializers import ThreadCreateSerializer, ThreadListSerializer, MessageCreateSerializer, \
    MessageListSerializer, MessageIsReadSerializer, UnreadMessageNumberListSerializer
from chat.models import Thread, Message

User = get_user_model()


class ThreadDeleteCreateApiView(CreateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Thread.objects.all()
    serializer_class = ThreadCreateSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user_id = request.user.id
        participants = [user_id, serializer.validated_data.pop('participant')]
        thread = Thread.objects.filter(
            participants=participants[0]).filter(
            participants=participants[-1]
        ).distinct().first()
        if thread:
            thread.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ThreadListApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ThreadListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(participants=user)


class MessageListCreateApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    create_serializer_class = MessageCreateSerializer
    list_serializer_class = MessageListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        else:
            return self.list_serializer_class

    def get_queryset(self):
        user = self.request.user
        thread = self.request.GET["thread"]
        return Message.objects.filter(thread__participants=user, thread=thread)


class MessageIsReadCreateApiView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageIsReadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        messages_list = serializer.validated_data.pop('messages')
        user = request.user
        messages = Message.objects.filter(
            thread__participants=user,
            id__in=messages_list,
            is_read=False
        ).exclude(
            sender=user
        )
        """From the point of view of security, it is better not to inform about the existence of the message"""
        for message in messages:
            message.is_read = True
            message.save()
        return Response(status=HTTP_200_OK)


class UnreadMessageNumberListApiView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnreadMessageNumberListSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

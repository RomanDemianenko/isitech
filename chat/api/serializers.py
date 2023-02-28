from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer, ValidationError

from chat.models import Thread, Message

User = get_user_model()


class ThreadCreateSerializer(ModelSerializer):
    participant = IntegerField(write_only=True)

    class Meta:
        model = Thread
        fields = (
            'id',
            'participant',
            'participants',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'participants',
        )

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        participants = [user_id, validated_data.pop('participant')]
        thread = Thread.objects.filter(
            participants=participants[0]).filter(
            participants=participants[-1]
        ).distinct().first()
        if thread:
            return thread
        thread_objects = Thread.objects.create()
        thread_objects.participants.set(participants)
        thread_objects.save()
        return thread_objects

    def validate_participant(self, value):
        user_id = self.context['request'].user.id
        participants = [user_id, value]
        if len(participants) > 2 or len(participants) == 1:
            raise ValidationError("The thread can be only between two users")

        elif len(set(participants)) < 2:
            raise ValidationError("The thread can be only between different users")

        return value


class ThreadListSerializer(ModelSerializer):
    message = SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'participants',
            'message',
            'created',
            'updated'
        )

    def get_message(self, instance):
        return Message.objects.filter(thread=instance.id).last()


class MessageCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'text',
            'thread',
        )

    def create(self, validated_data):
        text = validated_data['text']
        thread = validated_data['thread']
        sender = self.context['request'].user
        return Message.objects.create(text=text, thread=thread, sender=sender)

    def validate_thread(self, value):
        sender = self.context['request'].user
        if not Thread.objects.filter(id=value.id, participants=sender):
            raise ValidationError("You cannot send message in this thread")
        return value


class MessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'text',
            'thread',
            'created',
            'is_read',
        )


class MessageIsReadSerializer(ModelSerializer):
    messages = serializers.ListField()

    class Meta:
        model = Message
        fields = (
            'messages',
        )


class UnreadMessageNumberListSerializer(ModelSerializer):
    number_of_unread_message = SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'number_of_unread_message',
        )

    def get_number_of_unread_message(self, instance):
        user = self.context['request'].user
        return Message.objects.filter(
            thread__participants=user,
            is_read=False
        ).exclude(
            sender=user
        ).distinct().count()

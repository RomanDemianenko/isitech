from django.contrib import admin

from chat.models import Thread, User, Message

admin.site.register(User)
admin.site.register(Thread)
admin.site.register(Message)

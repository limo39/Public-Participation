from django.contrib import admin

# Register your models here.

from .models import Bill, Topic, Message, User


admin.site.register(User)
admin.site.register(Bill)
admin.site.register(Topic)
admin.site.register(Message)

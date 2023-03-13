from django.contrib import admin
from .models import PreviousChat, PreviousWriting

admin.site.register(PreviousChat)
admin.site.register(PreviousWriting)
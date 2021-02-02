from django.contrib import admin

from core.models import *

admin.register(Profile)(admin.ModelAdmin)
admin.register(Post)(admin.ModelAdmin)
admin.site.register(Notification)
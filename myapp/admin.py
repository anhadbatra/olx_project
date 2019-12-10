# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin, site
from .models import Advertise, UserDetail, Contact, Location, Category,MessageModel,Favorites


admin.site.register(Advertise)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(UserDetail)
admin.site.register(Contact)
admin.site.register(Favorites)

class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'

admin.site.register(MessageModel, MessageModelAdmin)


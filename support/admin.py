from django.contrib import admin
from .models import Ticket, Message


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'supporter', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'user__phone', 'supporter__phone')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at', 'is_support')
    list_filter = ('created_at', 'is_support')
    search_fields = ('ticket__subject', 'sender__phone', 'content')
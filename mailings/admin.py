from django.contrib import admin

from mailings.models import Recipient, Message, Newsletter


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "comment", "avatar",)
    list_filter = ("email",)
    search_fields = ("email", "full_name", "avatar",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "letter",)
    list_filter = ("subject",)
    search_fields = ("subject", "letter",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "first_shipment", "status", "message",)
    list_filter = ("recipients", "message",)
    search_fields = ("status", "message", "recipients",)

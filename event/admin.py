from django.contrib import admin
from .models import Event
# Register your models here.
@admin.register(Event)
class event_admin(admin.ModelAdmin):
    list_display =('id',"title", "category","slug")
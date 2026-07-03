from django.contrib import admin
from .models import Registration
# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display=['event','user','registered_at']
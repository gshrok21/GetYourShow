from django.contrib import admin

# Register your models here.
from .models import Invoice
@admin.register (Invoice)
class Invoice_admin(admin.ModelAdmin):
    list_display =("user","file")

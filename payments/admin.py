from django.contrib import admin
from .models import Payment
# Register your models here.
@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):
    list_display =('registration','amount', 'status')
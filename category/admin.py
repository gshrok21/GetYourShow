from django.contrib import admin
from .models import event_category
# Register your models here.
@admin.register(event_category)
class category_admin(admin.ModelAdmin):
    list_display=('id','name','slug')
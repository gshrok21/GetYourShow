from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser_details
# Register your models here.
@admin.register(CustomUser_details)
class user_admin(UserAdmin):
    model=CustomUser_details
    list_display=("id","mob","username")
    ordering=('username',"id")
    fieldsets=(("Details",{"fields":('username','password','mob','first_name','last_name')}),("Permissions",{'fields':('is_active',"is_seller","is_staff","is_superuser",'groups','user_permissions')}))
    add_fieldsets=((None,{"classes":("wide"),"fields":("mob","email",'username',"password1","password2")}),)

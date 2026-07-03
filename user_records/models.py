from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class userManager(BaseUserManager):
    def create_user(self,mob,password=None,**kwargs):
        if not mob:
            raise ValueError("Incorrect Mob. Number")
        else:
            user=self.model(mob=mob,**kwargs)
            user.set_password(password)
            user.save(using=self._db)
        return user
        
    def create_superuser(self,mob,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        return  self.create_user(mob,password,**kwargs)
        
class CustomUser_details(AbstractBaseUser,PermissionsMixin): 
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    mob=models.IntegerField(unique=True,null=True,blank=True)
    is_seller=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    USERNAME_FIELD='mob'
    REQUIRED_FIELD=['email','username']
    
    
    def __str__(self):
        return self.username
        
    objects=userManager()
    
    def has_perm(self,perm):
        return True
    def has_module_perms(self,app_label):
        return True

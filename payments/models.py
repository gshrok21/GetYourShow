from django.db import models

# Create your models here.
from django.conf import settings
from registration.models import Registration
class Payment(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'order_id : {self.order_id}'
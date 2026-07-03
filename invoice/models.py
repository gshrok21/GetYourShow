# yourapp/models.py

from django.db import models
from user_records.models import CustomUser_details as user
class Invoice(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id}"
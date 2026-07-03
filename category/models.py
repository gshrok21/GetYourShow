from django.db import models
from autoslug import AutoSlugField
# Create your models here.
class event_category(models.Model):
    name=models.CharField(max_length =100)
    slug=AutoSlugField(populate_from='name',unique=True)
    
    def __str__(self):
        return self.name
    
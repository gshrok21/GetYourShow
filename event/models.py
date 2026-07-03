from django.db import models
from user_records.models import CustomUser_details as User
from django.utils.text import slugify
from category.models import event_category
from autoslug import AutoSlugField

class Event(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title",unique=True, blank=True)
    description = models.TextField()

    category = models.ForeignKey(
        event_category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    location = models.CharField(max_length=300)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True, null=True)

    capacity = models.PositiveIntegerField(default=0, help_text="0 = unlimited")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    is_free = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
from django.db import models
from user_records.models import CustomUser_details as User
from event.models import Event   # assuming Event is in same app
import uuid
from django.utils import timezone
class Registration(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending Approval'),
        ('confirmed',  'Confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled',  'Cancelled'),
        ('attended',   'Attended'),
        ('no_show',    'No Show'),
    ]

    event           = models.ForeignKey(Event,      on_delete=models.CASCADE, related_name='registrations')
    user            = models.ForeignKey(User,       on_delete=models.CASCADE, related_name='registrations')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    order_id        = models.CharField(max_length=50,null=True, blank=True)
    amount_to_pay   = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid            = models.BooleanField(default=False)
    checked_in      = models.BooleanField(default=False)
    checked_in_at   = models.DateTimeField(null=True, blank=True)
    registered_at   = models.DateTimeField(auto_now_add=True)
    cancelled_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        #unique_together = ('event', 'user')
        ordering = ['-registered_at']
        
    def __str__(self):
        return f'{self.user.username} → {self.event.title} [{self.status}]'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def check_in(self):
        self.checked_in = True
        self.checked_in_at = timezone.now()
        self.status = 'attended'
        self.save()

    def cancel(self):
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.save()
        # Promote from waitlist
        waitlisted = Registration.objects.filter(
            event=self.event, status='waitlisted'
        ).order_by('registered_at').first()
        if waitlisted:
            waitlisted.status = 'confirmed'
            waitlisted.save()
            
    
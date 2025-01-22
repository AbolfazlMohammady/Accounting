from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES_UNREAD= "U"
    STATUS_CHOICES_IN_PROGRESS= "P"
    STATUS_CHOICES_CLOSED= "C"
    STATUS_CHOICES = [
        (STATUS_CHOICES_UNREAD, 'Unread'),
        (STATUS_CHOICES_IN_PROGRESS, 'In Progress'),
        (STATUS_CHOICES_CLOSED, 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', 
                            on_delete=models.PROTECT)
    
    supporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supported_tickets'
                                , null=True, blank=True, on_delete=models.PROTECT)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')

    def __str__(self):
        return self.subject


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_support = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} in ticket {self.ticket}'
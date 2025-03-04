from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Project(models.Model):
    title= models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_TASK = [
        ('P','Pending'),
        ('IP','In Progress'),
        ('C','Completed'),
        ('F','Failed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(max_length=2, choices=STATUS_TASK, default='P')
    start_time = models.DateTimeField(blank=True,null=True)
    due_time = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True,null=True)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0, validators=[MinValueValidator(-100), MaxValueValidator(100)])
    
    def clean(self):
        if self.assigned_user and self.assigned_user not in self.project.members.all():
            return ValidationError({'assigned_user': 'Assigned user must be a member of the project.'})
        if self.owner != self.project.owner:
            return ValidationError({'detail': "مالک تسک باید با مالک پروژه یکی باشد"})
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
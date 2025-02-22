from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
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
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('failed','Failed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(max_length=12, choices=STATUS_TASK, default='pending')
    start_time = models.DateTimeField(blank=True,null=True)
    due_time = models.DateTimeField(blank=True,null=True)
    completed_at = models.DateTimeField(blank=True,null=True)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0, validators=[MinValueValidator(-10), MaxValueValidator(10)])

    def __str__(self):
        return self.title
    
    # def save(self):
    #     if not self.start_time:
    #         self.start_time = timezone.now()
    #     if self.completed == True:
    #         self.completed_at = timezone.now()

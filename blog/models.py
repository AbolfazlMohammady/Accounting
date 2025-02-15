from django.db import models
from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('F', 'Football'),
        ('C', 'Coocki'),
        ('T', 'Teaching')
    ]
    STATUS_POST = [
        ('P', 'Published'),
        ('UR', 'Under Review'),
        ('R', 'Rejected')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    image = models.ImageField(upload_to='post', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_POST, default='UR', max_length=2)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name
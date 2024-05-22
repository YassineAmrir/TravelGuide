# notifications/models.py
from django.db import models

class Notification(models.Model):
    content = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.content

# voyages/models.py
from django.db import models

class Reservation(models.Model):
    client_name = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.client_name

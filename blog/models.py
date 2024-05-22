from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User
import uuid  # for generating confirmation numbers

class OffreVoyage(models.Model):
    GENRE_CHOICES = [
        ('Aventure', 'Aventure'),
        ('Culturel', 'Culturel'),
        ('Détente', 'Détente'),
        ('Sportif', 'Sportif'),
        ('Omra', 'Omra'),
        ('Haj', 'Haj'),
    ]
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    countries = models.CharField(max_length=255,default='')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_people = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='Aventure')
    speciale = models.BooleanField(default=False)
    hebergement = models.CharField(max_length=255, default='Hôtel')
    type_transport = models.CharField(max_length=255, default='Avion')
    compagnie_transport = models.CharField(max_length=255, default='Compagnie XYZ')
    

    def __str__(self):
        return self.title

class Image(models.Model):
    offre_voyage = models.ForeignKey(OffreVoyage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='site_images/', default='img/default_image.png')

    def __str__(self):
        return f'Image for {self.offre_voyage.title}'
    

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    offre_voyage = models.ForeignKey(OffreVoyage, on_delete=models.CASCADE)  

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    num_places = models.IntegerField()
    commentaire = models.TextField(blank=True, null=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.full_name} - {self.offre_voyage}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)  
    image = models.ImageField(upload_to='profile_images/', default='profile_images/profile.jpg') 

class Activite(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(default=0)
    lieu = models.CharField(max_length=255)
    participants_min = models.IntegerField(default=0)
    participants_max = models.IntegerField(default=0)
    image = models.ImageField(upload_to='activites/', null=True, blank=True)
    offre_voyage = models.ForeignKey('OffreVoyage', on_delete=models.CASCADE, related_name='activites', null=True, blank=True)
    prix_initial = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    prix_promo = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    def __str__(self):

        return self.nom



import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    confirmation_email_sent = models.BooleanField(default=False)
    confirmation_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def send_confirmation_email(self, email):
      print("Sending confirmation email...")
      if not self.confirmation_email_sent:
        subject = 'Payment Confirmation'
        message = f'Thank you for your payment of {self.amount} EUR. Confirmation Number: {self.confirmation_number}'
        from_email = 'radwaamli0@gmail.com'  # Replace with your email address
        recipient_list = [email]  # Pass a list with a single email address

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.confirmation_email_sent = True
            self.save()
        except Exception as e:
            # Handle exceptions, log errors, or perform additional actions
            print(f"Email sending failed: {str(e)}")
  
    def __str__(self):
        return f"{self.user.username} - {self.amount} EUR - Confirmation: {self.confirmation_number}"


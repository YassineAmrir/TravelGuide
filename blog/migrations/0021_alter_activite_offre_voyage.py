# Generated by Django 5.0 on 2024-02-03 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_activite_prix_promo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='offre_voyage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activites', to='blog.offrevoyage'),
        ),
    ]

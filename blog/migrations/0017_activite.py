# Generated by Django 5.0 on 2024-01-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_delete_book_offrevoyage_countries_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(default=0)),
                ('lieu', models.CharField(max_length=255)),
                ('participants_min', models.IntegerField(default=0)),
                ('participants_max', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='activites/')),
            ],
        ),
    ]

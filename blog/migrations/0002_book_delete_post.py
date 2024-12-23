# Generated by Django 5.0 on 2024-01-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('publish_date', models.DateField()),
                ('isbn_number', models.CharField(max_length=13)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]

# Generated by Django 3.2.22 on 2023-10-09 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthday',
            name='date_of_birth',
            field=models.DateField(verbose_name='%d-%m-%y'),
        ),
    ]

# Generated by Django 3.2.22 on 2023-10-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_birthday_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthday',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]

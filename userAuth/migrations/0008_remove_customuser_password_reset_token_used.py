# Generated by Django 5.2.1 on 2025-06-09 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0007_customuser_password_reset_token_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password_reset_token_used',
        ),
    ]

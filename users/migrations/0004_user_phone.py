# Generated by Django 5.0.2 on 2024-03-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]

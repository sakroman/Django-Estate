# Generated by Django 5.0.2 on 2024-03-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estates', '0002_remove_estate_agent_estate_listing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='garden',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estate',
            name='floor_area_sqm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='estate',
            name='land_area_sqm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]

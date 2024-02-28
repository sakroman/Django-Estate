from django.db import models
from users.models import User


class Estate(models.Model):

    PROPERTY_TYPES = (
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Apartment', 'Apartment'),
        ('Bungalow', 'Bungalow'),
        ('Terraced House', 'Terraced House'),
        ('Detached House', 'Detached House'),
        ('Semi-detached House', 'Semi-detached House'),
        ('Cottage', 'Cottage'),
        ('Farmhouse', 'Farmhouse'),
        ('Land', 'Land'),
        ('Commercial', 'Commercial'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Sold', 'Sold'),
    )


    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.BooleanField()
    floor_area_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    land_area_sqm = models.DecimalField(max_digits=10, decimal_places=2)

    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField()
    list_date = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.title

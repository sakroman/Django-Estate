from django.db import models
from users.models import User
from django.utils.safestring import mark_safe



class Estate(models.Model):
    LISTING_TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
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
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    title = models.CharField(max_length=300, blank=True, null=True, editable=False)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_type = models.CharField(max_length=100, choices=LISTING_TYPES)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.BooleanField()
    garden = models.BooleanField()
    floor_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_area_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField()
    list_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        self.title = f"{self.address}, {self.city}, {self.zipcode}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    estates = models.ManyToManyField(Estate)

    def __str__(self):
        return f"Saved properties for {self.user}"

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=50)
    listing_type = models.CharField(max_length=50)
    min_bedrooms = models.IntegerField(null=True, blank=True)
    max_bedrooms = models.IntegerField(null=True, blank=True)
    min_bathrooms = models.IntegerField(null=True, blank=True)
    max_bathrooms = models.IntegerField(null=True, blank=True)
    garage = models.BooleanField(null=True, blank=True)
    garden = models.BooleanField(null=True, blank=True)
    minPrice = models.IntegerField(null=True, blank=True)
    maxPrice = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_description(self):

        description = f"<span class='badge text-bg-info'>{self.property_type}</span>, <span class='badge text-bg-info'>{self.listing_type}</span>"
        if self.min_bedrooms is not None and self.min_bedrooms != 0:
            description += f", <span class='badge text-bg-info'>Min Bedrooms: {self.min_bedrooms}</span>"
        if self.max_bedrooms is not None and self.max_bedrooms != 6:
            description += f", <span class='badge text-bg-info'>Max Bedrooms: {self.max_bedrooms}</span>"
        if self.min_bathrooms is not None and self.min_bathrooms != 0:
            description += f", <span class='badge text-bg-info'>Min Bathrooms: {self.min_bathrooms}</span>"
        if self.max_bathrooms is not None and self.max_bathrooms != 6:
            description += f", <span class='badge text-bg-info'>Max Bathrooms: {self.max_bathrooms}</span>"
        if self.garage:
            description += f", <span class='badge text-bg-info'>Garage: {self.garage}</span>"
        if self.garden:
            description += f", <span class='badge text-bg-info'>Garden: {self.garden}</span>"
        if self.minPrice:
            description += f", <span class='badge text-bg-info'>Min Price: {self.minPrice}</span>"
        if self.maxPrice:
            description += f", <span class='badge text-bg-info'>Max Price: {self.maxPrice}</span>"
        return mark_safe(description)

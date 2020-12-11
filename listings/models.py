from django.db import models
from account.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# Create your models here.
class Property(models.Model):

    ROOM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12')
    )

    CATEGORY_CHOICES = (
        ("for_sale", "For Sale"),
        ("for_rent", "For Rent"),
        ("sold", "Sold")
    )

    TYPE_CHOICES = (
        ("townhomes", "Townhomes"),
        ("offices", "Offices"),
        ("single_family", "Single Family"),
        ("multi_family", "Multi Family"),
    )


    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length= 200, blank=True, null=True)
    address = models.CharField(max_length= 200, null=True, verbose_name='Property Address')
    description = RichTextField(null = True, unique=True, blank = True, verbose_name='Property Description')
    category = models.CharField(max_length= 100, null=True, choices=CATEGORY_CHOICES, verbose_name='Property Category')
    type = models.CharField(max_length= 100, null=True, choices=TYPE_CHOICES, verbose_name='Property Type')
    # promo_price = models.DecimalField(max_digits=19, decimal_places=2, null = True, verbose_name= _('Chapter number'))
    price = models.DecimalField(max_digits=19, decimal_places=2, null = True, verbose_name='Property Price')
    status = models.CharField(max_length= 200, null=True, default="active", verbose_name='Proprty Status')
    slug = models.SlugField(max_length=100, unique=True, null = True, blank = True)
    city = models.CharField(max_length= 200, null=True, verbose_name='Property City')
    featured_image = models.ImageField(upload_to="listings_upld/featured_image", height_field=None, width_field=None, max_length=100, null = True, verbose_name='Property Feature Image')
    # image_two = models.ImageField(upload_to="listings/gallery", height_field=None, width_field=None, max_length=100, null = True, blank = True)
    # image_three = models.ImageField(upload_to="listings/gallery", height_field=None, width_field=None, max_length=100, null = True, blank = True)
    # image_four = models.ImageField(upload_to="listings/gallery", height_field=None, width_field=None, max_length=100, null = True, blank = True)
    # gallery = models.CharField(max_length= 20000, blank=True, null=True)
    # longitude = models.CharField(max_length= 200, null=True)
    # latitude = models.CharField(max_length= 200, null=True)
    bedrooms = models.PositiveIntegerField(null=True, choices=ROOM_CHOICES, verbose_name='No. Bedrooms')
    bathrooms = models.PositiveIntegerField(null=True, choices=ROOM_CHOICES, verbose_name='No. Bathrooms')
    garage = models.PositiveIntegerField(null=True, choices=ROOM_CHOICES)
    area_size = models.CharField(max_length=100, blank=True, null=True, verbose_name='Area Size (sq ft)')
    # postal_code = models.CharField(max_length= 200, blank=True, null=True)
    published_on = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Properties"


    def __str__(self):
        return F"{self.address}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.address, allow_unicode=True)
        return super(Property, self).save(*args, **kwargs)


class Gallery(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="listings_upld/gallery", max_length=100, null = True, blank = True,
                                help_text="Select all images at once")

    class Meta:
        verbose_name_plural = "Gallery"

    def __str__(self):
        return F"{self.image}"

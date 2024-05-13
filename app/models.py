from django.db import models

class Product(models.Model):
    element_id = models.BigIntegerField(null=True, blank=False)
    title = models.CharField(null=True, blank=True, max_length=255)
    model = models.CharField(null=True, blank=True, max_length=64)
    brand = models.CharField(null=True, blank=True, max_length=64)
    color = models.CharField(null=True, blank=True, max_length=64)
    price = models.BigIntegerField(null=True, blank=True, default=0)
    category = models.CharField(null=True, blank=True, max_length=64)

    battery_range = models.CharField(null=True, blank=True, max_length=16) # km
    battery_capacity = models.CharField(null=True, blank=True, max_length=16) # kW

    remainder = models.IntegerField(null=True, blank=True, default=0) # остатка

    class Meta:
        pass


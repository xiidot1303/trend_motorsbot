from django.db import models

class Product(models.Model):
    element_id = models.BigIntegerField(null=True, blank=False)
    title = models.CharField(null=True, blank=True, max_length=255)
    model = models.CharField(null=True, blank=True, max_length=64)
    brand = models.CharField(null=True, blank=True, max_length=64)
    color = models.CharField(null=True, blank=True, max_length=64)
    price = models.BigIntegerField(null=True, blank=True, default=0)
    category = models.CharField(null=True, blank=True, max_length=64)
    description = models.TextField(null=True, blank=True, max_length=2048, default='')
    photo = models.FileField(null=True, blank=True, upload_to='photos')

    battery_range = models.CharField(null=True, blank=True, max_length=16) # km
    battery_capacity = models.CharField(null=True, blank=True, max_length=16) # kW

    remainder = models.IntegerField(null=True, blank=True, default=0) # остатка

    class Meta:
        pass


class Order_item(models.Model):
    product = models.ForeignKey('app.Product', null=True, blank=True, on_delete=models.PROTECT)
    price = models.BigIntegerField(null=True, blank=True, default=0)

    class Meta:
        pass


class Order(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', null=True, blank=True, on_delete=models.PROTECT)
    personal_data = models.JSONField(null=True, blank=True)
    order_item = models.ForeignKey('app.Order_item', null=True, blank=True, on_delete=models.PROTECT)
    contract = models.FileField(null=True, blank=True, upload_to='contract')
    datetime = models.DateTimeField(null=True, db_index=True, auto_now_add=True)
    
class Passport_data(models.Model):
    serial = models.CharField(null=True, blank=False, max_length=8)
    number = models.CharField(null=True, blank=False, max_length=16)
    birth_date = models.DateField(null=True, blank=True)

    # personal data
    pnfl = models.CharField(null=True, blank=False, max_length=16)
    surname = models.CharField(null=True, blank=False, max_length=32)
    name = models.CharField(null=True, blank=False, max_length=32)
    patronym = models.CharField(null=True, blank=False, max_length=32)
    birth_place = models.CharField(null=True, blank=False, max_length=32)
    nationality = models.CharField(null=True, blank=False, max_length=32)


    


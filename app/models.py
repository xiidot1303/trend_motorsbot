from django.db import models

class Product(models.Model):
    element_id = models.BigIntegerField(null=True, blank=False)
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name="Название")
    model = models.CharField(null=True, blank=True, max_length=64, verbose_name="Модель")
    brand = models.CharField(null=True, blank=True, max_length=64, verbose_name="Марка")
    color = models.CharField(null=True, blank=True, max_length=64, verbose_name="Цвет")
    price = models.BigIntegerField(null=True, blank=True, default=0, verbose_name="Цена")
    category = models.CharField(null=True, blank=True, max_length=64, verbose_name="Категория")
    description = models.TextField(null=True, blank=True, max_length=2048, default='', verbose_name="Описание")
    photo = models.FileField(null=True, blank=True, upload_to='photos', verbose_name="Фото")

    battery_range = models.CharField(null=True, blank=True, max_length=16, verbose_name="Диапазон аккумулятора") # km
    battery_capacity = models.CharField(null=True, blank=True, max_length=16, verbose_name="Емкость батарей") # kW

    remainder = models.IntegerField(null=True, blank=True, default=0, verbose_name="Остаток") # остатка

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Order_item(models.Model):
    product = models.ForeignKey('app.Product', null=True, blank=True, on_delete=models.PROTECT)
    price = models.BigIntegerField(null=True, blank=True, default=0)

    class Meta:
        pass

class Order(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', null=True, blank=True, on_delete=models.PROTECT)
    passport_data = models.ForeignKey('app.Passport_data', null=True, blank=True, on_delete=models.PROTECT)
    order_item = models.ForeignKey('app.Order_item', null=True, blank=True, on_delete=models.PROTECT)
    contract = models.FileField(null=True, blank=True, upload_to='contract')
    amocrm_lead_id = models.BigIntegerField(null=True, blank=True)
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
    doc_give_place = models.CharField(null=True, blank=False, max_length=255)
    date_begin_document = models.DateField(null=True, blank=True)

    
class Branch(models.Model):
    title = models.CharField(null=True, blank=False, max_length=255)
    REGIION_CHOICES = [
        ('andijan', 'Andijon viloyati'),
        ('bukhara', 'Buxoro viloyati'),
        ('fergana', 'Farg‘ona viloyati'),
        ('jizzakh', 'Jizzax viloyati'),
        ('kashkadarya', 'Qashqadaryo viloyati'),
        ('khorezm', 'Xorazm viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('navoiy', 'Navoiy viloyati'),
        ('samarkand', 'Samarqand viloyati'),
        ('sirdaryo', 'Sirdaryo viloyati'),
        ('surkhandarya', 'Surxondaryo viloyati'),
        ('tashkent', 'Toshkent viloyati'),
        ('karakalpakstan', 'Qoraqalpog‘iston Respublikasi'),
        ('tashkent_city', 'Toshkent')
    ]
    region = models.CharField(null=True, blank=True, max_length=64, choices=REGIION_CHOICES)

class Vin_code(models.Model):
    element_id = models.BigIntegerField(null=True, blank=False)
    full_title = models.CharField(null=True, blank=True, max_length=255)
    code = models.CharField(null=True, blank=True, max_length=64)
    product = models.ForeignKey('app.Product', null=True, blank=True, on_delete=models.PROTECT)
    branch_title = models.CharField(null=True, blank=True, max_length=255)


class Contracts(models.Model):
    user = models.ForeignKey("bot.Bot_user", null=False, blank=False, on_delete=models.CASCADE)
    one_c_id = models.CharField(null=False, blank=False, max_length=64, unique=True, verbose_name="1C id")
    one_c_uidd = models.CharField(null=False, blank=False, max_length=255, unique=True, verbose_name="1C uidd")
    car = models.CharField(null=False, blank=False, max_length=255, verbose_name="Машина")
    quantity = models.IntegerField(null=False, blank=False, verbose_name="Количество")
    price = models.BigIntegerField(null=False, blank=False, verbose_name="Цена")
    created = models.DateField(auto_now_add=True, verbose_name="Создано")
    pay_date = models.DateField(null=True, blank=True, verbose_name="Срок оплаты")
    installment = models.BooleanField(default=False, null=False, blank=False, verbose_name="Рассрочка")

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"

    def __str__(self):
        return self.car


class PayHistory(models.Model):
    contract = models.ForeignKey('app.Contracts', null=False, blank=False, on_delete=models.CASCADE)
    one_c_id = models.BigIntegerField(null=False, blank=False, verbose_name="1C id")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    amount = models.BigIntegerField(null=False, blank=False, verbose_name="Сумма")
    currency = models.CharField(null=True, blank=True, max_length=4, verbose_name="Валюта")

    class Meta:
        verbose_name = "История оплаты"
        verbose_name_plural = "История оплат"

    def __str__(self):
        return self.contract.car


class PaySchedule(models.Model):
    contract = models.OneToOneField('app.Contracts', on_delete=models.CASCADE, related_name='pay_schedule')
    pay_date = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name="Следующая дата оплаты")
    file_id = models.CharField(null=True, blank=True, max_length=255, verbose_name="TG file id")
    json = models.JSONField(null=False, blank=False)

    class Meta:
        verbose_name = "График оплаты"
        verbose_name_plural = "График оплат"

    def __str__(self):
        return self.contract.car

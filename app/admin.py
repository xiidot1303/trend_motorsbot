from django.contrib import admin
from app.models import *

class ProductAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

admin.site.register(Product, ProductAdmin)
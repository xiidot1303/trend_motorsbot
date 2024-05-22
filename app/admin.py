from django.contrib import admin
from app.models import *

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class Passport_dataAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class BranchAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class Vin_codeAdmin(admin.ModelAdmin):
    search_fields = ['product__id']
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

admin.site.register(Product, ProductAdmin)
admin.site.register(Passport_data, Passport_dataAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Vin_code, Vin_codeAdmin)
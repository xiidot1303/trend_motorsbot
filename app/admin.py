from django.contrib import admin
from app.models import *
from django.utils.html import format_html
from django.urls import reverse

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display_links = None
    list_filter = ['brand', 'color', 'category']
    list_display = [
        'title', 'model', 'brand', 'color', 'price', 'category', 
        'description', 'open_photo', 'battery_range', 'battery_capacity',
        'remainder', 'edit_button'
    ]
    
    def edit_button(self, obj):
        change_url = reverse('admin:app_product_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i></a>', change_url)
    edit_button.short_description = 'Действие'

    def open_photo(self, obj):
        if obj.photo:
            change_url = f'/files/{obj.photo}'
            return format_html('<a target="_blank" class="btn btn-success" href="{}"><i class="fas fa-eye"></i></a>', change_url)
        return None
    open_photo.short_description = 'Фото'

    fieldsets = (
        ('', {
            'fields': [
                'title', 'model', 'brand', 'color', 'price', 'category', 
                'description', 'photo', 'battery_range', 'battery_capacity',
                'remainder'
                ],
            'description': ''
        }),
    )

class OrderAdmin(admin.ModelAdmin):
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
admin.site.register(Order, OrderAdmin)
admin.site.register(Passport_data, Passport_dataAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Vin_code, Vin_codeAdmin)
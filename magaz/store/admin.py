from django.contrib import admin
from .models import Category, Product, ProductExtraImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'product_count']
    list_display_links = None
    list_editable = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return len(obj.products.all())
    product_count.short_description = 'Кол-во товаров'


class ProductExtraImageInline(admin.TabularInline):
    model = ProductExtraImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'image', 'avaible', 'new']
    list_editable = ['price', 'image', 'avaible', 'new']
    list_filter = ['category', 'avaible', 'new']
    radio_fields = {'category': admin.HORIZONTAL}
    prepopulated_fields = {'slug': ('name', 'category')}
    search_fields = ['name', 'description']
    inlines = [ProductExtraImageInline]

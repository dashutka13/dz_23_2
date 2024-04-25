from django.contrib import admin

from catalog.models import Category, Product, Blog, Version


# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_title', 'is_published',)
    list_filter = ('blog_title',)
    search_fields = ('blog_title', 'body',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product', 'is_active',)
    list_filter = ('name', 'product', 'is_active',)
    search_fields = ('name', 'num', 'product',)

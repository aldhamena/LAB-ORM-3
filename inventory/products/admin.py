from django.contrib import admin
from .models import Product, Review, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):

    list_display = ("title", "supplier", "rating")
    list_filter = ("rating",)


class ReviewAdmin(admin.ModelAdmin):

    list_display =  ("name", "product", "rating")
    list_filter = ("product", "rating")

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
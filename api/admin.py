from django.contrib import admin

# Register your models here.
from api.models import Category, Food, Delivery


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
        fields = '__all__'

admin.site.register(Category, CategoryAdmin)


class FoodAdmin(admin.ModelAdmin):
    class Meta:
        model = Food
        fields = '__all__'

admin.site.register(Food, FoodAdmin)


class DeliveryAdmin(admin.ModelAdmin):
    class Meta:
        model = Delivery
        fields = '__all__'

admin.site.register(Delivery, DeliveryAdmin)
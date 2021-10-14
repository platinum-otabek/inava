from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import CustomUser, SlugModel

UserAdmin.fieldsets = (
        (_('Foydalanuvchini tahrirlash'), {'fields': ('username', 'password', 'name', 'is_staff', 'is_active')}),
)

UserAdmin.add_fieldsets = (
    (None, {'fields': ('username', 'password1', 'password2', 'name', 'is_staff', 'is_active')}),
)


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'name', 'is_restaurant', 'is_staff', 'is_active']
    list_filter = ['is_restaurant', 'is_active']
    class Meta:
        model = CustomUser
        fields = '__all__'


admin.site.register(CustomUser, CustomUserAdmin)


# chernovek
class SlugAdmin(admin.ModelAdmin):
    class Meta:
        model = SlugModel
        fields = '__all__'

admin.site.register(SlugModel, SlugAdmin)
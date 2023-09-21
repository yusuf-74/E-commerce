from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User,Address,PhoneNumber,OneTimePassCode,AuthProvider


class CustomUserChangeFrom(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"
        
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeFrom
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active','is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields",
        {
            "fields": (
                "is_verified",
                "role"
            ),
        },
    ),)


admin.site.register(User,CustomUserAdmin)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(OneTimePassCode)
admin.site.register(AuthProvider)
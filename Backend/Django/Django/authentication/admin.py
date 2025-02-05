from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Extend the default UserAdmin to include the custom fields like `role`
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # Adding `role` to the user form inside the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

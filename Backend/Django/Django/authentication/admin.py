from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Quiz
from .models import QuizResponse



# Extend the default UserAdmin to include the custom fields like `role`
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('first_name', 'last_name', 'username', 'email', 'role', 'is_staff', 'is_active')
    
    # Adding `role`, 'firsst_name', 'last_name' to the user form inside the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'due_date', 'is_published', 'teacher') 
    list_filter = ('is_published', 'due_date') 
    search_fields = ('title', 'description')  

# Register the Quiz model
admin.site.register(Quiz, QuizAdmin)

admin.site.register(QuizResponse)

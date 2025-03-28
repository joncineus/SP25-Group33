from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Quiz
from .models import QuizResponse
from .models import Question



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


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_text_short', 'question_type', 'correct_answer_display')
    list_filter = ('quiz', 'question_type')
    search_fields = ('question_text',)
    fieldsets = (
        (None, {
            'fields': ('quiz', 'question_text', 'question_type')
        }),
        ('Multiple Choice Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer_mc'),
            'classes': ('collapse',),
        }),
        ('Written Answer', {
            'fields': ('correct_answer_written',),
            'classes': ('collapse',),
        }),
    )

    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'
    
    def correct_answer_display(self, obj):
        if obj.question_type == 'MC':
            return f"{obj.correct_answer_mc}: {getattr(obj, f'option_{obj.correct_answer_mc.lower()}')}"
        return obj.correct_answer_written[:50] + '...' if obj.correct_answer_written else None
    correct_answer_display.short_description = 'Correct Answer'

admin.site.register(Question, QuestionAdmin)
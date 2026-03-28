from django.contrib import admin
# Đảm bảo đủ 7 class được import ở đây
from .models import Course, Lesson, Question, Choice, Enrollment, Instructor, Learner, Submission

# 1. Implementation của ChoiceInline
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

# 2. Implementation của QuestionInline
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# 3. Implementation của QuestionAdmin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'lesson']
    search_fields = ['question_text']

# 4. Implementation của LessonAdmin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

# Đăng ký các model vào admin site
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission) # Phải có dòng này để lấy trọn 3 điểm

import core.models
import django.contrib

django.contrib.admin.site.register(core.models.Book)


class LectureInline(django.contrib.admin.TabularInline):
    model=core.models.Lecture
    extra=40

class CourseAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('semester', 'year', 'department', 'number')
    list_filter = ['semester', 'year', 'department', 'number']
    inlines = [LectureInline]

django.contrib.admin.site.register(core.models.Course, CourseAdmin)

class QuestionAdmin(django.contrib.admin.ModelAdmin):
    fieldsets = [
    (None,       {'fields': ['question', 'answer']}), 
    ('Metadata', {'fields': ['points', 'category', 'lecture']}),
    ('Resource', {'fields': ['book', 'section', 'index']})]
    
django.contrib.admin.site.register(core.models.Question,
                                   QuestionAdmin)



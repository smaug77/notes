import core.models
import django.contrib


class ConceptAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('name', 'section')

django.contrib.admin.site.register(core.models.Concept, ConceptAdmin)

django.contrib.admin.site.register(core.models.Book)


class SectionInline(django.contrib.admin.TabularInline):
    model = core.models.Section
    extra = 40


class CourseAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('name', 'semester', 'year', 'department', 'number')
    list_filter = ['name', 'semester', 'year', 'department', 'number']
    inlines = [SectionInline]

django.contrib.admin.site.register(core.models.Course, CourseAdmin)


class QuestionAdmin(django.contrib.admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['question', 'answer']}),
        ('Metadata', {'fields': ['points', 'category', 'section']}),
        ('Resource', {'fields': ['book', 'book_section', 'index']})]

django.contrib.admin.site.register(core.models.Question,
                                   QuestionAdmin)

import core.models
import django.contrib

django.contrib.admin.site.register(core.models.Book)
django.contrib.admin.site.register(core.models.Lecture)
django.contrib.admin.site.register(core.models.Course)
django.contrib.admin.site.register(core.models.Question)


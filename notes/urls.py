from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^core/$', 'core.views.index'),
    url(r'^core/test_view/(?P<course_id>\d+)/$',
        'core.views.test_view'),
    url(r'^core/books/$', 'core.views.book_list'),
    url(r'^core/book/(?P<book_id>\d+)/$', 'core.views.book'),
    url(r'^core/course/(?P<course_id>\d+)/$', 'core.views.course'),
    url(r'^admin/', include(admin.site.urls)),
)

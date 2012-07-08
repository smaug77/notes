from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^test_view/(?P<course_id>\d+)/$',
        'test_view'),
    url(r'^books/$', 'book_list'),
    url(r'^book/(?P<book_id>\d+)/$', 'book'),
    url(r'^course/(?P<course_id>\d+)/$', 'course'),
    url(r'^new_concepts/$', 'new_concept'),
)

"""
    core.views
    ----------

    

"""


import django.shortcuts
import django.http
import core.models
def index(request):
    test_list = core.models.Course.objects.all()
    return django.shortcuts.render_to_response('core/index.html',
                                               {'test_list': test_list})

def test_view(request, course_id):
    c = django.shortcuts.get_object_or_404(core.models.Course,
                                           pk=course_id)
    return django.shortcuts.render_to_response('core/test.html',
                                               {'course': c})


def book_list(request):
    book_list = core.models.Book.objects.all()
    return django.shortcuts.render_to_response('core/book_list.html',
                                               {'book_list': book_list})

def book(request, book_id):
    b = django.shortcuts.get_object_or_404(core.models.Book,
                                           pk=book_id)
    return django.shortcuts.render_to_response('core/book.html',
                                               {'book': b})

def course(request, course_id):
    c = django.shortcuts.get_object_or_404(core.models.Course,
                                           pk=course_id)
    return django.shortcuts.render_to_response('core/course.html',
                                               {'course': c})


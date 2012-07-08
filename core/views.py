"""
    core.views
    ----------

    

"""
import django.shortcuts
import django.http
import core.models
import logging

logger = logging.getLogger('django.request')

def index(request):
    test_list = core.models.Course.objects.all()
    book_list = core.models.Book.objects.all()
    return django.shortcuts.render_to_response('core/index.html',
                                               {'test_list':
                                                test_list,
                                                   'book_list':
                                                   book_list,
                                                   })

def test_view(request, course_id):
    c = django.shortcuts.get_object_or_404(core.models.Course,
                                           pk=course_id)
    l = django.shortcuts.get_list_or_404(core.models.Section,
                                           course=course_id)
    questions = []
    for lecture in l:
        questions += lecture.question_set.all()
    points = sum( [x.points for x in questions] )
    return django.shortcuts.render_to_response('core/test.html',
                                               {'course': c,
                                                'lectures': l,
                                                'questions':
                                                questions,
                                                'points': points,
                                                   })



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
                                               {'course': c},
                                               context_instance=django.template.RequestContext(request)
        )

def new_concept(request):
    try:
        new_texts = request.POST.getlist('concept')
        section_id = request.POST['section']
        s = django.shortcuts.get_object_or_404(core.models.Section,
                                           pk=section_id)
    except KeyError:
        c = s.course
        return django.shortcuts.render_to_response('core/course.html',
                                                   {'course': c},
                                                   context_instance=django.template.RequestContext(request)
            )
    else:
        for new_text in new_texts:
            if new_text != '':
                nc = core.models.Concept(name=new_text,section=s)
                nc.save()
        return django.http.HttpResponseRedirect(
            django.core.urlresolvers.reverse('core.views.course',
                                             args=(s.course.pk,)))
    


"""
    core.views
    ----------

    

"""
import django.shortcuts
import django.http
import core.models
import logging
from copy import deepcopy

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('notes')

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
    l = core.models.Section.objects.filter(course=course_id).order_by('number')
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
                                                   {'course': c,
                                                    'error_message':
                                                    "No Concepts Entered"},
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

def question_edit(request, course_id, section_id):
  try:  
    c = django.shortcuts.get_object_or_404(core.models.Course,
                                           pk=course_id)
    s = django.shortcuts.get_object_or_404(core.models.Section,
                                           pk=section_id)
    book_list = core.models.Book.objects.all()   
    cpts = s.concept_set.all()
    print s
    print s.question_set.all()
    l = core.models.Section.objects.filter(course=course_id).order_by('number')
    # what type of course is it?
    lecture = l[0]
    if (l.category == 'L'):
       course_total = 1050
    elif (l.category == 'W'):
       course_total = 525
    elif (l.category == 'U'):
       course_total = 180
    sections = len(l)
    points_budget = int(course_total/sections)
    points_total = sum([x.points for x in s.question_set.all()])
    points_exer = sum([x.points for x in s.question_set.all() if x.category=='X'])
    points_other = sum([x.points for x in s.question_set.all() if x.category!='X'])
    return django.shortcuts.render_to_response('core/question_edit.html',
                                               {'course': c,
                                                'section': s,
                                                'points_budget': points_budget,
                                                'book_list':book_list,
                                                'points_total': points_total,
                                                'points_exer': points_exer,
                                                'points_other': points_other,
                                                'concepts': cpts},
                                               context_instance=django.template.RequestContext(request))
  except:
    logger.exception("something went wrong")
    
def new_question(request, course_id, section_id):
    logger.info("in new_question")
    try:
        logger.info("%s" % request.POST)
        question_dict = {}
        concepts = []
        for k,v in request.POST.items():
            if k == u'concept':
                concepts = \
                [django.shortcuts.get_object_or_404(core.models.Concept,
                                                    pk=int(i)) for i
                                                    in v]
            elif k != u'csrfmiddlewaretoken':
                question_dict[k] = v
        #        question_dict = deepcopy(request.POST)

        book_id = request.POST['book'][0]
        if book_id != u'':
            question_dict['book'] = django.shortcuts.get_object_or_404(core.models.Book,
                                               pk=int(book_id))
            logger.info("created %s of type %s" %
                        (question_dict['book'],
                         type(question_dict['book'])))
            logger.info("%s" % question_dict)
        else:
            question_dict['book'] = None
    except:
        logger.exception("failed to create book instance for %s" % request.POST)
        c = django.shortcuts.get_object_or_404(core.models.Course,
                                               pk=course_id)
        s = django.shortcuts.get_object_or_404(core.models.Section,
                                               pk=section_id)
        book_list = core.models.Book.objects.all()   
        cpts = s.concept_set.all()
        points_used = sum([x.points for x in s.question_set.all()])
        return django.shortcuts.render_to_response('core/question_edit.html',
                                                   {'course': c,
                                                    'section': s,
                                                    'book_list':book_list,
                                                    'points_used': points_used,
                                                    'concepts': cpts,                                                    
                                                    'error_message':
                                                    "No Book Selected"},
            context_instance=django.template.RequestContext(request))

    question_dict['section_id'] = section_id
    try:
        new_question = core.models.Question(**(question_dict))
        new_question.save()
        for x in concepts:
            new_question.concepts.add(x)
        new_question.save()
    except:
        logger.exception("Failed to create a new question:")

    django.http.HttpResponseRedirect(
            django.core.urlresolvers.reverse('core.views.question_edit',
                                             args=(course_id, section_id,)))

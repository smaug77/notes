"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django.test as d_test
import core.models

class CoreViewsIndexTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_basic(self):
        resp = self.client.get('/core/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('test_list' in resp.context)
        self.assertEqual([course.pk for course in
                         resp.context['test_list']], [1])
        course_1 = resp.context['test_list'][0]
        self.assertEqual(course_1.name, 'Linear Algebra')
        self.assertEqual(course_1.semester, 'F')
        self.assertEqual(course_1.year, 1995)
        self.assertEqual(course_1.department, 'M')
        self.assertEqual(course_1.number, 215)
        self.assertTrue('book_list' in resp.context)
        self.assertEqual([book.pk for book in
                         resp.context['book_list']], [1])
        book_1 = resp.context['book_list'][0]
        self.assertEqual(book_1.title, u'Elementary Linear Algebra')
        self.assertEqual(book_1.author, 'Howard Anton')
        self.assertEqual(book_1.edition, '') 
        
class CoreViewsTestViewTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_basic_question(self):
        resp = self.client.get('/core/test_view/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('questions' in resp.context)
        self.assertEqual([question.pk for question in
                         resp.context['questions']], [1])
        question_1 = resp.context['questions'][0]
        self.assertEqual(question_1.points, 1)
        self.assertEqual(question_1.category, 'D')
        self.assertEqual(question_1.question, u'Define when two vectors '\
                         'are equivalent.')
        self.assertEqual(question_1.answer, u'When they have the '\
                         'same length and same direction, even if '\
                         'the initial andterminal points are not the '\
                         'same.\r\n')
        self.assertEqual(question_1.section.pk, 1)
        self.assertEqual(question_1.book.pk, 1)
        self.assertEqual(question_1.book_section, '3.1')
        
    def test_basic_course(self):
        resp = self.client.get('/core/test_view/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('course' in resp.context)
        course_1 = resp.context['course']
        self.assertEqual(course_1.name, 'Linear Algebra')
        self.assertEqual(course_1.semester, 'F')
        self.assertEqual(course_1.year, 1995)
        self.assertEqual(course_1.department, 'M')
        self.assertEqual(course_1.number, 215)

    def test_failure(self):
        resp = self.client.get('/core/test_view/2/')
        self.assertEqual(resp.status_code, 404)
        
class CoreViewsBookListTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_basic(self):
        resp = self.client.get('/core/books/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('book_list' in resp.context)
        self.assertEqual([book.pk for book in
                         resp.context['book_list']], [1])
        book_1 = resp.context['book_list'][0]
        self.assertEqual(book_1.title, u'Elementary Linear Algebra')        
        self.assertEqual(book_1.author, 'Howard Anton')
        self.assertEqual(book_1.edition, '')
        
class CoreViewsBookTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_basic(self):
        resp = self.client.get('/core/book/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('book' in resp.context)
        book_1 = resp.context['book']
        self.assertEqual(book_1.title, u'Elementary Linear Algebra')        
        self.assertEqual(book_1.author, 'Howard Anton')
        self.assertEqual(book_1.edition, '')

    def test_failure(self):
        resp = self.client.get('/core/book/2/')
        self.assertEqual(resp.status_code, 404)
    
class CoreViewsCourseTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']
    
    def test_basic(self):
        resp = self.client.get('/core/course/1/')
        self.assertEqual(resp.status_code, 200)
        course_1 = resp.context['course']
        self.assertEqual(course_1.name, 'Linear Algebra')
        self.assertEqual(course_1.semester, 'F')
        self.assertEqual(course_1.year, 1995)
        self.assertEqual(course_1.department, 'M')
        self.assertEqual(course_1.number, 215)
        
    def test_failure(self):
        resp = self.client.get('/core/course/3/')
        self.assertEqual(resp.status_code, 404)

class CoreNewConceptTest(d_test.TestCase):
    fixtures = ['core_views_testdata.json']

    def test_good_concept(self):
        section_1 = core.models.Section.objects.get(pk=1)
        resp = self.client.post('/core/new_concepts/', {'concept':
        ['Definition of something', 'Theorem on something else'],
        'section': 1})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/core/course/1/')
        self.assertEqual(section_1.concept_set.get(pk=1).name,
                         "Definition of something")
        self.assertEqual(section_1.concept_set.get(pk=1).section,
                         section_1)
        self.assertEqual(section_1.concept_set.get(pk=2).name,
                         "Theorem on something else")
        self.assertEqual(section_1.concept_set.get(pk=2).section,
                         section_1)

    def test_no_post_data(self):
        resp = self.client.post('core/new_concepts')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['error_message'],
                         "No Concepts Entered")
        
        

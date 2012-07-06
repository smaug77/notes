from django.db import models

# strangely, django seems to suggest having unit tests here.
from django.utils import unittest

class Course(models.Model):
    """A course

       instance variables
       ------------------
       
       * name - string
       * semester - either winter, spring, summer or fall
       * year
       * department - math, physics, etc.
       * number       
       
       methods
       -------

       * full_name - returns a name including course number,
                     department, etc.       

    """
    
    SEMESTERS = (
        ('W', 'Winter'),
        ('P', 'Spring'),
        ('U', 'Summer'),
        ('F', 'Fall'),
        )

    DEPTS = (
        ('M', 'Math'),
        ('P', 'Physics'),
        ('H', 'Philosophy'),
        ('E', 'Economics'),
        ('C', 'Computer Science'),
        ('S', 'Sociology'),
        )

    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=2, choices=SEMESTERS)
    year = models.PositiveIntegerField()
    department = models.CharField(max_length=2, choices=DEPTS)
    number = models.PositiveIntegerField()

    def full_name(self):
        return "%s %d: %s" % (self.get_department_display(),
                              self.number, self.name)

    def __unicode__(self):
        return self.full_name()

class CourseTestCase(unittest.TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(name="Linear Algebra",
                                            semester="F", year=1995,
                                            department="M",
                                            number=215)
        
    def test_full_name(self):
        self.assertEqual(self.course1.full_name(), u"Math 215: Linear" +
                         u" Algebra")
        

class Lecture(models.Model):
    """A Lecture

       instance variables
       ------------------

       * number
       * course - reference to a course
       * title  - string
    """

    number = models.PositiveIntegerField()
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s %s" % (str(self.course), str(self.number))

class Book(models.Model):
    """A book

       instance variables
       ------------------
       
       * title
       * author
       * edition - optional
    """

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    edition = models.CharField(max_length=3, blank=True)

    def __unicode__(self):
        return "%s by %s" % (self.title, self.author)
    

class Question(models.Model):
    """A question and answer.

       This is the root datum in the notes module and other apps will
       most likely use this or run analytics.

       instance variables
       ------------------

       * points      - how many points (i.e. minutes) for this
                       question.
       * category    - is this testing statements, examples, proofs, etc.
       * question    - (LaTeX) string
       * answer      - (LaTex) string
       * lecture     - reference to the lecture in a course. (and a
                       lecture references a course, of course).
       * book        - reference to a Book that this came from. This may
                       be None.
       * section     - string which is the section in the book. This
                       may be None
       * index       - string which is the problem, theorem number
                       etc. in book ref. This may be None.
    """

    TYPES = (
        ('C', 'Concept'),
        ('S', 'Statement'),
        ('D', 'Definition'),
        ('E', 'Example'),
        ('P', 'Proof'),
        ('X', 'Exercise'),
    )

    points = models.PositiveIntegerField()
    category = models.CharField(max_length=2, choices=TYPES)
    question = models.TextField()
    answer = models.TextField()
    lecture = models.ForeignKey(Lecture)
    book = models.ForeignKey(Book, blank=True)
    section = models.CharField(max_length=10, blank=True)
    index = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return "%s %s" % (str(self.lecture), str(self.category))

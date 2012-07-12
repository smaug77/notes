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

    SEMESTERS = (('W', 'Winter'),
                 ('P', 'Spring'),
                 ('U', 'Summer'),
                 ('F', 'Fall'))

    DEPTS = (
        ('M', 'Math'),
        ('P', 'Physics'),
        ('H', 'Philosophy'),
        ('E', 'Economics'),
        ('C', 'Computer Science'),
        ('S', 'Sociology'))

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

    def test_unicode(self):
        self.assertEqual(unicode(self.course1), u"Math 215: Linear" +
                         u" Algebra")


class Section(models.Model):
    """A section of a course. This could a lecture, week, etc. The
       type will determine the length of the review. Each section gets
       about 20 minutes. So:

       ========= =============================
       Type      Total Review Time
       ========= =============================
       Lecture   800 minutes or 2 weeks review
       Week      360 minutes or 1 week review
       Unit      120 minutes or 1/3 week review
       ========= =============================

       instance variables
       ------------------

       * number
       * course - reference to a course
       * title  - string
       * type   - Lecture
    """

    TYPES = (
        ('L', 'Lecture'),
        ('W', 'Week'),
        ('U', 'Unit'))

    number = models.PositiveIntegerField()
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=TYPES)

    def __unicode__(self):
        return "%s %s: %s" % (str(self.course), str(self.number),
                              str(self.title))


class SectionTestCase(unittest.TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(name="Linear Algebra",
                                             semester="F", year=1995,
                                             department="M",
                                             number=215)
        self.section1 = Section.objects.create(number=1,
                                               course=self.course1,
                                               title='Linear' +
                                               ' Algebra',
                                               category='L')

    def test_unicode(self):
        self.assertEqual(unicode(self.section1),
                         u"Math 215: Linear Algebra 1: Linear Algebra")


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


class Concept(models.Model):
    """A concept in a class

       instance variables
       ------------------

       * name - string
       * section
    """

    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section)


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
       * section     - reference to the section in a course. (and a
                       section references a course, of course).
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
    section = models.ForeignKey(Section)
    book = models.ForeignKey(Book, blank=True)
    book_section = models.CharField(max_length=10, blank=True)
    index = models.CharField(max_length=20, blank=True)
    concepts = models.ManyToManyField(Concept)

    def __unicode__(self):
        return "%s %s" % (str(self.section), self.get_category_display())


class QuestionTestCase(unittest.TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(name="Linear Algebra",
                                             semester="F", year=1995,
                                             department="M",
                                             number=215)
        self.section1 = Section.objects.create(number=1,
                                               course=self.course1,
                                               title='Linear' +
                                               ' Algebra',
                                               category='L')
        self.book1 = Book.objects.create(title="Elementary", author="Anton")
        self.question1 = Question.objects.create(points=1,
                                                 category='D',
                                                 question="What is X?",
                                                 answer="Y!",
                                                 section=self.section1,
                                                 book=self.book1,
                                                 book_section='',
                                                 index='1.1',)

    def test_unicode(self):
        self.assertEqual(unicode(self.question1),
                         u"Math 215: Linear Algebra 1: " +
                         u"Linear Algebra Definition")

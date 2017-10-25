from django.test import TestCase

from universities.models import University
from .models import Campus, School
from .resources import CampusResource, SchoolResource


class CampusTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')

    def test_add(self):
        resource = CampusResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        campus = Campus.objects.all().last()
        self.assertEqual(campus.name, 'foo')

    def test_update(self):
        Campus.objects.create(uni=self.uni, name='foo')
        resource = CampusResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        campuses = Campus.objects.all()
        self.assertEqual(len(campuses), 1)


class SchoolTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')

    def test_add(self):
        resource = SchoolResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        school = School.objects.all().last()
        self.assertEqual(school.name, 'foo')

    def test_update(self):
        School.objects.create(uni=self.uni, name='foo')
        resource = SchoolResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        schools = School.objects.all()
        self.assertEqual(len(schools), 1)


class CourseTests(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='foo')

    def test_add(self):
        resource = SchoolResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        school = School.objects.all().last()
        self.assertEqual(school.name, 'foo')

    def test_update(self):
        School.objects.create(uni=self.uni, name='foo')
        resource = SchoolResource()
        result = resource.import_csv('"name"\n"foo"', self.uni)
        self.assertFalse(result.has_errors())
        schools = School.objects.all()
        self.assertEqual(len(schools), 1)

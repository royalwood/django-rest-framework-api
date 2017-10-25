from django.test import TestCase

from .models import University


class UniversityTest(TestCase):
    def test_create(self):
        University.objects.create(name="Test Uni", code="TU001", state="VIC", short_name="TU")

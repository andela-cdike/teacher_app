from django.test import TestCase

from factories import factories


class ClassModelTestSuite(TestCase):

    def test_class_model(self):
        test_class = factories.ClassFactory()
        self.assertEqual(str(test_class), test_class.name)

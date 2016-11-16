from django.test import TestCase

from factories import factories


class ClassModelTestSuite(TestCase):

    def test_class_model(self):
        test_class = factories.ClassFactory()
        self.assertEqual(str(test_class), test_class.name)


class StudentModelTestSuite(TestCase):

    def test_student_model(self):
        student = factories.StudentFactory()
        self.assertEqual(
            str(student),
            '{0} {1} {2}'.format(
                student.first_name,
                student.middle_name,
                student.last_name
            )
        )


class SubjectModelTestSuite(TestCase):

    def test_subject_model(self):
        subject = factories.SubjectFactory()
        self.assertEqual(str(subject), subject.title)

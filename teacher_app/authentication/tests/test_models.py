from django.test import TestCase

from factories import factories


class TeacherModelTestSuite(TestCase):

    def test_teacher_model(self):
        teacher = factories.TeacherFactory()
        self.assertEqual(
            str(teacher),
            '{0} {1}'.format(teacher.first_name, teacher.last_name)
        )

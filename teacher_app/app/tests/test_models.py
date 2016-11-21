from django.test import TestCase

from app import models
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


class ScoreSheetModelTestSuite(TestCase):

    def setUp(self):
        student_a = factories.StudentFactory()
        subject_a = factories.SubjectFactory()
        subject_b = factories.SubjectFactory()
        self.score_sheet_a = factories.ScoreSheetFactory(
            student=student_a, subject=subject_a, score=70
        )
        self.score_sheet_b = factories.ScoreSheetFactory(
            student=student_a, subject=subject_b, score=60
        )
        self.edited_student = models.Student.objects.get(pk=student_a.pk)

    def test_score_sheet_model(self):
        score_sheet = factories.ScoreSheetFactory()
        self.assertIsInstance(score_sheet.subject, models.Subject)
        self.assertIsInstance(score_sheet.student, models.Student)

    def test_student_total_is_calculated_accurately(self):
        self.assertEqual(
            self.edited_student.total,
            self.score_sheet_a.score + self.score_sheet_b.score
        )

    def test_student_average_is_calculated_accurately(self):
        expected_average = (
            self.score_sheet_a.score + self.score_sheet_b.score) / 2
        self.assertEqual(self.edited_student.average, expected_average)

    def test_class_total_is_calculated_accurately(self):
        student_b = factories.StudentFactory(
            my_class=self.score_sheet_a.student.my_class)
        subject_c = factories.SubjectFactory()
        score_sheet_c = factories.ScoreSheetFactory(
            student=student_b, subject=subject_c, score=50
        )
        expected_total = (
            self.score_sheet_a.score +
            self.score_sheet_b.score +
            score_sheet_c.score
        )
        self.assertEqual(
            self.edited_student.my_class.total,
            expected_total
        )

    def test_class_average_is_calculated_accurately(self):
        student_b = factories.StudentFactory(
            my_class=self.score_sheet_a.student.my_class)
        subject_c = factories.SubjectFactory()
        score_sheet_c = factories.ScoreSheetFactory(
            student=student_b, subject=subject_c, score=50
        )
        expected_total = (
            self.score_sheet_a.score +`
            self.score_sheet_b.score +
            score_sheet_c.score
        )
        expected_average = expected_total / float(3)
        self.assertEqual(
            self.edited_student.my_class.average, expected_average)

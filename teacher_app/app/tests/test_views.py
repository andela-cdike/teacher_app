from django.test import Client, TestCase
from django.urls import reverse

from authentication.models import Teacher
from app.models import Class, Student
from factories import factories


class Base(TestCase):

    def setUp(self):
        self.teacher = factories.TeacherFactory()
        self.client = Client()
        self.client.login(
            username=self.teacher.username, password=factories.PASSWORD
        )


class IndexViewTestSuite(Base):

    def setUp(self, *args, **kwargs):
        super(IndexViewTestSuite, self).setUp(*args, **kwargs)
        self.class_a = factories.ClassFactory(teacher=self.teacher)
        self.class_b = factories.ClassFactory(teacher=self.teacher)
        self.class_c = factories.ClassFactory(teacher=self.teacher)

    def test_user_is_able_to_view_classes(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.class_a.name, response.content)
        self.assertIn(self.class_b.name, response.content)
        self.assertIn(self.class_c.name, response.content)

    def test_unauthenticated_user_cannot_access_page(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)


class ClassViewsTestSuite(Base):

    def setUp(self, *args, **kwargs):
        super(ClassViewsTestSuite, self).setUp(*args, **kwargs)
        self.class_a = factories.ClassFactory(teacher=self.teacher)

    def test_create_class(self):
        url = reverse('create-class')
        data = {'name': 'class A'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        new_class = Class.objects.filter(name=data['name'])
        self.assertTrue(new_class.exists())
        self.assertIsInstance(new_class[0].teacher, Teacher)

    def test_view_students_in_class(self):
        self.student_a = factories.StudentFactory(my_class=self.class_a)
        self.student_b = factories.StudentFactory(my_class=self.class_a)

        url = reverse('class-detail', kwargs={'pk': self.class_a.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.student_a), response.content)
        self.assertIn(str(self.student_b), response.content)

    def test_add_student_to_class(self):
        url = reverse('create-student', kwargs={'pk': self.class_a.pk})
        data = {
            'first_name': 'John',
            'middle_name': 'Junior',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        student = Student.objects.filter(first_name=data['first_name'])
        self.assertTrue(student.exists())
        self.assertEqual(student[0].my_class, self.class_a)

    def test_edit_class_name(self):
        url = reverse('edit-class', kwargs={'pk': self.class_a.pk})
        data = {'name': 'edit class'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        edited_class = Class.objects.filter(name=data['name'])
        self.assertTrue(edited_class.exists())

    def test_edit_class_name_to_a_used_name(self):
        class_b = factories.ClassFactory(teacher=self.teacher)
        url = reverse('edit-class', kwargs={'pk': self.class_a.pk})
        data = {'name': class_b.name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', response.content)


class StudentViewTestSuite(Base):

    def setUp(self):
        super(StudentViewTestSuite, self).setUp()
        class_a = factories.ClassFactory(teacher=self.teacher)
        self.student = factories.StudentFactory(my_class=class_a)

    def test_view_students_subjects(self):
            self.physics = factories.SubjectFactory(students=(self.student,))
            self.chemistry = factories.SubjectFactory(students=(self.student,))

            url = reverse(
                'student-detail',
                kwargs={
                    'class_id': self.student.my_class.pk,
                    'pk': self.student.pk
                }
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.physics.title, response.content)
            self.assertIn(self.chemistry.title, response.content)

    def test_edit_student(self):
        url = reverse(
            'edit-student',
            kwargs={
                'class_id': self.student.my_class.id,
                'pk': self.student.id
            }
        )
        data = {
            'first_name': 'John',
            'middle_name': 'Junior',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        edited_student = Student.objects.get(pk=self.student.pk)
        self.assertEqual(edited_student.first_name, data['first_name'])
        self.assertEqual(edited_student.last_name, data['last_name'])
        self.assertEqual(edited_student.middle_name, data['middle_name'])

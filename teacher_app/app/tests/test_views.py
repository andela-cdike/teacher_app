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
        class_a = Class.objects.filter(name=data['name'])
        self.assertTrue(class_a.exists())
        self.assertIsInstance(class_a[0].teacher, Teacher)

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

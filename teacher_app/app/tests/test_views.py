from django.test import Client, TestCase
from django.urls import reverse

from authentication.models import Teacher
from app.models import Class
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


class ClassViewTestSuite(Base):

    def setUp(self, *args, **kwargs):
        super(ClassViewTestSuite, self).setUp(*args, **kwargs)

    def test_create_class(self):
        url = reverse('create-class')
        data = {'name': 'class A'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        class_a = Class.objects.filter(name=data['name'])
        self.assertTrue(class_a.exists())
        self.assertIsInstance(class_a[0].teacher, Teacher)

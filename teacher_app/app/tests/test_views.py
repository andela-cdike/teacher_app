from django.test import Client, TestCase
from django.urls import reverse

from factories import factories


class IndexViewTestSuite(TestCase):

    def setUp(self):
        teacher = factories.TeacherFactory()
        self.class_a = factories.ClassFactory(teacher=teacher)
        self.class_b = factories.ClassFactory(teacher=teacher)
        self.class_c = factories.ClassFactory(teacher=teacher)
        self.client = Client()
        self.client.login(
            username=teacher.username, password=factories.PASSWORD
        )

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

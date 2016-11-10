from django.test import Client, TestCase
from django.urls import reverse

from factories import factories


class RegisterViewTestSuite(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        url = reverse('register')
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'username': 'john_doe@test.com',
            'password1': 'testing123',
            'password2': 'testing123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Successfully registered', response.cookies)

    def test_register_with_short_password(self):
        url = reverse('register')
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'username': 'john_doe@test.com',
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'authentication/register.html')
        self.assertIn('Error', response.content)

    def test_register_with_password_confirmation_mismatch(self):
        url = reverse('register')
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'username': 'john_doe@test.com',
            'password1': 'mismatch',
            'password2': 'mixmatch'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'authentication/register.html')
        self.assertIn('Error', response.content)

    def test_register_with_duplicate_username(self):
        teacher = factories.TeacherFactory()
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe1',
            'username': teacher.username,
            'password1': 'testing12345',
            'password2': 'testing12345'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'authentication/register.html')
        self.assertIn('Error', response.content)

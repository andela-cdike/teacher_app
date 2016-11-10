from django.test import Client, TestCase
from django.urls import reverse

from factories import factories


class Base(TestCase):

    def setUp(self):
        self.template_name = 'authentication/authentication.html'


class RegisterViewTestSuite(Base):

    def setUp(self):
        super(RegisterViewTestSuite, self).setUp()
        self.client = Client()

    def test_register_success(self):
        url = reverse('register')
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'username': 'john_doe@test.com',
            'password1': factories.PASSWORD,
            'password2': factories.PASSWORD
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('You have been successfully registered',
                      response.cookies.get('messages').value)

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
        self.assertEqual(response.template_name[0], self.template_name)
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
        self.assertEqual(response.template_name[0], self.template_name)
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
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertIn('Error', response.content)


class LoginViewTestSuite(Base):

    def setUp(self):
        super(LoginViewTestSuite, self).setUp()
        self.teacher = factories.TeacherFactory()
        self.client = Client()

    def test_login_route(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        url = reverse('login')
        data = {
            'username': self.teacher.username,
            'password': factories.PASSWORD
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username,
                         self.teacher.username)

    def test_login_with_wrong_username(self):
        url = reverse('login')
        data = {
            'username': 'fake_user',
            'password': factories.PASSWORD
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertIn('Error', response.content)

    def test_login_with_wrong_password(self):
        url = reverse('login')
        data = {
            'username': self.teacher.username,
            'password': 'fake_password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template_name)
        self.assertIn('Error', response.content)

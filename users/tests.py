from django.test import TestCase, RequestFactory, Client
from users.views import (
    logout_user,
    profiles
)
from trade_simulation.models import (
    User
)

LOGIN_URL = "/users/login/"
REGISTER_URL = "/users/register/"
LOGOUT_URL = "/users/logout/"


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='test_user',
                                                  email='test@user.com',
                                                  password='12345')

    def test_login_page(self):
        """
        Test that we can log in
        """
        # GIVEN
        response = self.client.get(LOGIN_URL)
        # WHEN/THEN
        self.assertEqual(response.status_code, 200)

    def test_login_not_exits(self):
        """
        Test that we can not log in
        """
        # GIVEN
        response = self.client.post(LOGIN_URL, {'username': 'test_fail', 'password': 'test'})
        # WHEN/THEN
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        """
        Test that failing log in
        """
        # GIVEN
        response = self.client.post(LOGIN_URL, {'username': self.test_user.username, 'password': '12345'})
        # WHEN/THEN
        self.assertEqual(response.status_code, 302)


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='test_user',
                                                  email='test@user.com',
                                                  password='12345')

    def test_register_page(self):
        """
        Test that we render register page
        """
        # GIVEN
        response = self.client.get(REGISTER_URL)
        # WHEN/THEN
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Test that we can register
        """
        # GIVEN
        response = self.client.post(REGISTER_URL, {'username': 'testuser', 'password1': 'test123456', 'password2': 'test123456'})
        # WHEN/THEN
        self.assertEqual(response.status_code, 302)

    def test_register_fail(self):
        """
        Test that we can not register
        """
        # GIVEN
        response = self.client.post(REGISTER_URL, {'username': 'testfail', 'password1': '12345', 'password2': 'test12345'})
        # WHEN/THEN
        self.assertEqual(response.status_code, 200)


class ProfilesTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_profiles_page(self):
        """
        Test that we render profiles page
        """
        # GIVEN
        request = self.factory.get('/')
        # WHEN/THEN
        self.assertEqual(profiles(request).status_code, 200)


class LogoutTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_logout_page(self):
        """
        Test that we render logout
        """
        # GIVEN
        User.objects.create_superuser('admin', 'foo@foo.com', 'admin')
        self.client.login(username='admin', password='admin')
        response = self.client.get("/users/logout/")
        # WHEN/THEN
        self.assertEqual(response.status_code, 302)

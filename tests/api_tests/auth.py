__author__ = 'Jableader'
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

GET_AUTH_TOKEN_ = '/auth/get-token/'


class TokenTests(APITestCase):
    def test_can_get_login_token(self):
        self.bob = User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post(GET_AUTH_TOKEN_, {'username': 'Bob', 'password': 'bobs_password'}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data['token'])

    def test_invalid_user_gets_error(self):
        response = self.client.post(GET_AUTH_TOKEN_, {'username': 'Nobody', 'password': 'blah'}, format='json')

        self.assertEqual(400, response.status_code)

    def test_wrong_password_gets_error(self):
        User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post(GET_AUTH_TOKEN_, {'username': 'Bob', 'password': 'not_bobs_password'}, format='json')

        self.assertEqual(400, response.status_code)

    def test_token_auth_is_setup(self):
        bob = User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        token = Token.objects.create(user=bob)

        auth = "Token " + token.key

        response = APIClient().get('/hello-world/', follow=True, HTTP_AUTHORIZATION=auth)

        self.assertEqual(b'hello Bob', response.content)

    def test_can_auth_with_token(self):
        User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post(GET_AUTH_TOKEN_, {'username': 'Bob', 'password': 'bobs_password'}, format='json')
        token = response.data['token']

        auth = 'Token ' + token

        token_client = APIClient()
        response = token_client.get('/hello-world/', follow=True, HTTP_AUTHORIZATION=auth)

        self.assertEqual(b'hello Bob', response.content)


REGISTER_USER_ = '/auth/register'


class RegisterUserTest(APITestCase):

    def test_can_register(self):
        username, email, password = 'Bob', 'bob@email.com', 'bobs_password'
        data = {'username':username, 'email':email, 'password':password}

        response = self.client.put(REGISTER_USER_, data=data)
        self.assertEqual(201, response.status_code)

        user = User.objects.get(username=username)
        self.assertIsNotNone(user, 'User should have been created')
        self.assertEqual(email, user.email, 'User should have the supplied email')
        self.assert_(user.check_password(password), 'User should have the supplied password')

    def test_bad_email(self):
        username, email, password = 'Bob', 'bobsemail.com', 'bobs_password'
        data = {'username':username, 'email':email, 'password':password}

        response = self.client.put(REGISTER_USER_, data=data)

        self.assertEqual(400, response.status_code)

    def test_used_username(self):
        username, email, password = 'Bob', 'bob@email.com', 'bobs_password'
        data = {'username':username, 'email':email, 'password':password}

        User.objects.create_user(username, 'unique@email.com', 'shittypassword')

        response = self.client.put(REGISTER_USER_, data)

        self.assertEqual(400, response.status_code)

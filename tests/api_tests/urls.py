__author__ = 'Jableader'
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

class ApiUrlsTest(APITestCase):
    def test_can_get_login_token(self):
        self.bob = User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post('/get-auth-token/', {'username': 'Bob', 'password': 'bobs_password'}, format='json')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data['token'])

    def test_invalid_user_gets_error(self):
        response = self.client.post('/get-auth-token/', {'username': 'Nobody', 'password': 'blah'}, format='json')

        self.assertEqual(400, response.status_code)

    def test_wrong_password_gets_error(self):
        User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post('/get-auth-token/', {'username': 'Bob', 'password': 'not_bobs_password'}, format='json')

        self.assertEqual(400, response.status_code)

    def test_token_auth_is_setup(self):
        bob = User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        token = Token.objects.create(user=bob)

        auth = "Token " + token.key

        response = APIClient().get('/hello-world/', follow=True, HTTP_AUTHORIZATION=auth)

        self.assertEqual(b'hello Bob', response.content)

    def test_can_auth_with_token(self):
        User.objects.create_user(username='Bob', email='bob@nope.com', password='bobs_password')
        response = self.client.post('/get-auth-token/', {'username': 'Bob', 'password': 'bobs_password'}, format='json')
        token = response.data['token']

        auth = 'Token ' + token

        token_client = APIClient()
        response = token_client.get('/hello-world/', follow=True, HTTP_AUTHORIZATION=auth)

        self.assertEqual(b'hello Bob', response.content)

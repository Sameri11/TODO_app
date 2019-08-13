from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from todos.models import Tasks


def get_tokens_for_user(self, user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserTestCase(APITestCase):
    def test_create_account(self):
        url = reverse('register')
        data = {
            "username": "Fil",
            "email": "fil@fil.com",
            "password": "1234567898",
            "first_name": "Filly",
            "last_name": "Willy"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TokenTestCase(APITestCase):
    def test_get_token(self):
        User.objects.create_user('skijl', 'adf@ru.ru', '123456')
        url = reverse('token_obtain_pair')
        data = {
            "username": "skijl",
            "password": "123456"
        }
        response = self.client.post(url, data, format='json')
        json_response = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return json_response['refresh']

    def test_refresh_token(self):
        token = self.test_get_token()
        data = {'refresh': token}
        url = reverse('token_refresh')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return response.data['access']


class CreateTaskTestCase(APITestCase):
    def test_not_authenticated(self):
        url = reverse('new_task')
        data = {'1': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        User.objects.create_user('skij', 'adf@ru.ru', '123456')
        user = User.objects.get(pk=1)
        token = get_tokens_for_user(self, user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        url = reverse('new_task')
        data = {
            "task_name": "TODO: updated(updated again: only name)"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateTaskTestCase(APITestCase):
    def test_not_authenticated(self):
        User.objects.create_user('skij', 'adf@ru.ru', '123456')
        user = User.objects.get(username='skij')
        Tasks.objects.create(user=user, task_name='TODO')
        pk = Tasks.objects.get(task_name='TODO').pk
        url = 'http://127.0.0.1:8000/api/v1/task/updated/' + str(pk)
        data = {'1': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        User.objects.create_user('skil', 'adf@ru.ru', '123456')
        user = User.objects.get(username='skil')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(user=user, task_name='TODO')
        pk = Tasks.objects.get(task_name='TODO').pk
        url = 'http://127.0.0.1:8000/api/v1/task/updated/' + str(pk)
        data = {
            'task_name': 'TODO-new'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Tasks.objects.get(task_name='TODO-new'))


class ListViewTestCase(APITestCase):
    def test_not_authenticated(self):
        url = reverse('task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        User.objects.create_user('ski', 'adf@ru.ru', '123456')
        user = User.objects.get(username='ski')
        token = get_tokens_for_user(self, user=user)['access']
        url = reverse('task_list')
        Tasks.objects.create(user=user, task_name='TODO')
        Tasks.objects.create(user=user, task_name='TODOMS')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminListViewTestCase(APITestCase):
    def test_not_authenticated(self):
        url = reverse('admin_task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated(self):
        User.objects.create_superuser('admin', 'admin@admin.com', '123456')
        user = User.objects.get(username='admin')
        token = get_tokens_for_user(self, user=user)['access']
        url = reverse('admin_task_list')
        Tasks.objects.create(user=user, task_name='TODO')
        Tasks.objects.create(user=user, task_name='TODOMS')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteTaskViewTestCase(APITestCase):
    def test_not_authenticated(self):
        User.objects.create_user('skp', 'adf@ru.ru', '123456')
        user = User.objects.get(username='skp')
        Tasks.objects.create(user=user, task_name='TODO')
        pk = Tasks.objects.get(task_name='TODO').pk
        url = 'http://127.0.0.1:8000/api/v1/task/destroyed/' + str(pk) + '/'
        data = {'id': pk}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated(self):
        User.objects.create_user('skp', 'adf@ru.ru', '123456')
        user = User.objects.get(username='skp')
        token = get_tokens_for_user(self, user=user)['access']
        Tasks.objects.create(user=user, task_name='TODO')
        pk = Tasks.objects.get(task_name='TODO').pk
        url = 'http://127.0.0.1:8000/api/v1/task/destroyed/' + str(pk) + '/'
        data = {'id': pk}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# Create your tests here.

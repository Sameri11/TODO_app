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


def make_user(self, username, password):
    user = User.objects.create_user(username, password)
    return user


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


class TasksViewSetTestCase(APITestCase):
    def test_list_view(self):
        url = reverse('tasks-list')
        user = make_user(self, 'skilk', '123456')
        token = get_tokens_for_user(self, user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view(self):
        url = reverse('tasks-list')
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        data = {
            "title": "New Task"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_view(self):
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(user=user, title='TODO')
        pk = Tasks.objects.get(title='TODO').pk
        url = reverse('tasks-detail', args=[pk])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_view(self):
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(user=user, title='TODO')
        pk = Tasks.objects.get(title='TODO').pk
        url = reverse('tasks-detail', args=[pk])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_view(self):
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(
            user=user,
            title='TODO',
            status=3,
            priority=3)
        url = reverse('tasks-list') + '?status=3&priority=3'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Tasks.objects.get(title='TODO'))

    def test_partial_update_view(self):
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(user=user, title='TODO')
        pk = Tasks.objects.get(title='TODO').pk
        url = reverse('tasks-detail', args=[pk])
        data = {
            "description": "Wow!"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Wow!', response.data['description'])

    def test_update_view(self):
        user = make_user(self, 'skim', '123456')
        token = get_tokens_for_user(self, user)['access']
        Tasks.objects.create(user=user, title='TODO')
        pk = Tasks.objects.get(title='TODO').pk
        url = reverse('tasks-detail', args=[pk])
        data = {
            "title": 'New TODO',
            "description": "Wow!",
            "status": 3,
            "priority": 3
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Wow!', response.data['description'])


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
        Tasks.objects.create(user=user, title='TODO')
        Tasks.objects.create(user=user, title='TODOMS')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

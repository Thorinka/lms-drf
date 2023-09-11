import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.

class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='Adminov',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )

        self.user.set_password('123456')
        self.user.save()

        self.course = Course.objects.create(
            name='test',
            description='test_description',
        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='test_desc_lesson',
            video='https://www.youtube.com/sdsddwdw',
            course=self.course,
        )
        response = self.client.post('/users/token/', {'email': 'admin@admin.ru', 'password': '123456'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_list(self):
        """ Test for getting list of lessons """

        response = self.client.get(
            reverse('myapp:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "test_lesson",
                        "course": "test"
                    },
                ]
            }
        )

    def test_post_create(self):
        """ Test for creating new lesson """

        data = {
            'name': 'test_lesson2',
            'description': 'test_desc_lesson2',
            'video': 'https://www.youtube.com/3123f12312',
            'course': self.course.id
        }

        response = self.client.post(
            '/lessons/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_update(self):
        """ Test for patching lesson """

        data = {
            'name': 'test_lesson_updated',
            'description': 'test_desc_lesson2_updated',
            'video': 'https://www.youtube.com/3123f12312',
            'course': self.course.id,
        }
        response = self.client.put(
            reverse('myapp:lesson_update', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        self.client.delete(
            reverse('myapp:lesson_delete', args=[self.lesson.id])
        )

        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='Adminov',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )

        self.user.set_password('123456')
        self.user.save()

        self.course = Course.objects.create(
            name='test',
            description='test_description',
        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='test_desc_lesson',
            video='https://www.youtube.com/sdsddwdw',
            course=self.course,
        )

        response = self.client.post('/users/token/', {'email': 'admin@admin.ru', 'password': '123456'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_subscription(self):
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post(
            reverse('myapp:subscription_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_subscription(self):
        self.client.delete(
            reverse('myapp:subscription_delete', args=[self.course.id])
        )

        self.assertFalse(Subscription.objects.filter(id=self.course.id).exists())

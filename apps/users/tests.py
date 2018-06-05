from django.test import TestCase
from rest_framework.test import APIRequestFactory


class DevicesTests(TestCase):
    def setUp(self):
        print('start.....')
        factory = APIRequestFactory()
        request = factory.get('/devices/')
        print(request)
        print('start.....')

    def test_count(self):
        print('test.....')
        print('test.....')

    def tearDown(self):
        print('end.....')
        print('end.....')

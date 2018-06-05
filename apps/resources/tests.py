from rest_framework.test import APITestCase


class ResourceTests(APITestCase):
    def setUp(self):
        print('start.....')
        response = self.client.get('http://118.24.157.119:8000/resource/', format='json')
        print(response)
        print(dir(response))
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.data.get('count'), 1)
        print('start.....')

    def test_count(self):
        print('test.....')
        print('test.....')

    def tearDown(self):
        print('end.....')
        print('end.....')

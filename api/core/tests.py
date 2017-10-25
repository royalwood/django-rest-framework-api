from rest_framework.test import APITestCase
from rest_framework import status


class AdminTests(APITestCase):
    def test_up(self):
        response = self.client.get('/ucroo-admin-382/login/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DocsTests(APITestCase):
    def test_up(self):
        response = self.client.get('/api-docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

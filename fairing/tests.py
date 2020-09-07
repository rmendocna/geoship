from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.


class URLTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_api_ships(self):
        url = reverse('api-fairing-ship-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_api_bad_positions(self):
        url = reverse('api-fairing-ship-position-list', kwargs={'imo': '123456789'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)


import json

from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from .models import Ship


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

    def test_api_positions(self):
        url = reverse('api-fairing-ship-position-list', kwargs={'imo': '9632179'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_api_unknown_ship_positions(self):
        url = reverse('api-fairing-ship-position-list', kwargs={'imo': '9632177'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)


class OutputTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_api_positions(self):
        url = reverse('api-fairing-ship-position-list', kwargs={'imo': '9632179'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 517)
        self.assertEqual(content[0]['latitude'], 51.8737335205078)

    def _add_ship(self):
        new_data = dict(
            imo='7528843', name='RESOLVE PIONEER', ship_type='1005',
        )
        new_ship = Ship(**new_data)
        new_ship.save()

    def test_api_ship_positions(self):
        self._add_ship()
        url = reverse('api-fairing-ship-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 4)

    def test_import_positions(self):
        self._add_ship()
        call_command('load_positions', 'fairing/fixtures/resolve_pioneer.csv')
        url = reverse('api-fairing-ship-position-list', kwargs={'imo': '9632179'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 517)
        self.assertEqual(content[0]['latitude'], 51.8737335205078)


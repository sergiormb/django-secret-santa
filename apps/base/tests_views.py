# -*- coding: utf-8 -*-
from faker import Faker

from django.test import Client, TestCase

from base.models import User


class HomeViewTest(TestCase):

    def test_home_page(self):
        c = Client()  # instantiate the Django test client
        response = c.get('/')
        self.assertContains(response, 'Secret Santa')


class LoginViewTest(TestCase):

    def setUp(self):
        fake_search = Faker()
        fake = fake_search.profile(fields=None, sex=None)
        self.username = fake['username']
        self.email = fake['mail']
        self.password = self.username
        User.objects.create_user(self.username, self.email, self.password)

    def test_secure_page(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/inscriptions')
        self.assertContains(response, self.username)

    def test_no_login_page(self):
        response = self.client.get('/inscriptions', follow=True)
        self.assertEqual(response.status_code, 404)

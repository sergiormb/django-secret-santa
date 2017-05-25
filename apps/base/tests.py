# -*- coding: utf-8 -*-
from faker import Faker

from base.models import User, Group, Inscription
from django.db import IntegrityError

from django.test import TestCase


class InscriptionsTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(password="test", username="spino")
        Group.objects.create(creator=user1, name="Prueba")
        Group.objects.create(creator=user1, name="Prueba2")

    def test_create_inscription(self):
        """A user joins a group"""
        user1 = User.objects.get(username="spino")
        group = Group.objects.get(name="Prueba")
        Inscription.objects.create(user=user1, group=group)

    def test_create_multiple_inscription(self):
        """A user tries to sign up multiple times in a group"""
        user1 = User.objects.get(username="spino")
        group = Group.objects.get(name="Prueba")
        Inscription.objects.create(user=user1, group=group)
        with self.assertRaises(IntegrityError):
            Inscription.objects.create(user=user1, group=group)

    def test_create_multiple_inscription_diferent_groups(self):
        """A user tries to sign up multiple times in a group"""
        user1 = User.objects.get(username="spino")
        group = Group.objects.get(name="Prueba")
        group2 = Group.objects.get(name="Prueba2")
        Inscription.objects.create(user=user1, group=group)
        Inscription.objects.create(user=user1, group=group2)

    def test_create_multiple_delete_inscription(self):
        """
        A user tries to register multiple times in a group
        by deleting one of their inscriptions first
        """
        user1 = User.objects.get(username="spino")
        group = Group.objects.get(name="Prueba")
        inscription = Inscription.objects.create(user=user1, group=group)
        inscription.delete()
        Inscription.objects.create(user=user1, group=group)


class GroupTestCase(TestCase):

    def setUp(self):
        fake = Faker()
        user1 = User.objects.create(password="test", username="spino")
        group = Group.objects.create(creator=user1, name="Prueba")
        for i in range(10):
            user_fake = fake.profile(fields=None, sex=None)
            user = User.objects.create(password=user_fake['mail'], username=user_fake['username'])
            Inscription.objects.create(user=user, group=group)

    def test_close_group(self):
        """Close group"""
        group = Group.objects.get(name="Prueba")
        group.close_group()
        inscriptions = Inscription.objects.filter(group=group)
        for inscription in inscriptions:
            self.assertNotEqual(inscription.user, inscription.give_gift.user)
        self.assertEqual('close', group.status)

    def test_move_bag_withot_close_group(self):
        """Move bag without close group"""
        group = Group.objects.get(name="Prueba")
        group.move_bag()
        inscriptions = Inscription.objects.filter(group=group)
        for inscription in inscriptions:
            self.assertEqual(None, inscription.give_gift)
        self.assertEqual('open', group.status)

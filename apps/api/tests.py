from faker import Faker

from django.urls import reverse
from django.db.models import Q

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from base.models import User, Group, Inscription


class SecretSantaTestCase(APITestCase):

    def setUp(self):
        super(SecretSantaTestCase, self).setUp()
        fake = Faker()
        for i in range(3):
            user_fake = fake.profile(fields=None, sex=None)
            user = User.objects.create(username=user_fake['username'], email=user_fake['mail'])
            user.set_password(user_fake['username'])
            user.save()
        self.user = user
        self.user2 = User.objects.filter(~Q(username=self.user.username))[0]
        self.group = Group.objects.create(creator=user, name="Test")
        for user in User.objects.all():
            Inscription.objects.create(group=self.group, user=user)

    def check_page_without_login(self, url, pk=None):
        if pk:
            url = reverse(url, args=(pk,))
        else:
            url = reverse(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def check_page_with_login(self, url, pk=None):
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        if pk:
            url = reverse(url, args=(pk,))
        else:
            url = reverse(url)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupAPITests(SecretSantaTestCase):

    def test_list_groups_check_page_without_login(self):
        """
        List groups without login
        """
        self.check_page_without_login('groups_list_api')

    def test_list_groups_with_login(self):
        """
        List groups with login
        """
        self.check_page_with_login('groups_list_api')

    def test_new_group_check_page_without_login(self):
        """
        New group without login
        """
        url = reverse('groups_list_api')
        data = {'name': 'Test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_new_group_with_login(self):
        """
        New group with login
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('groups_list_api')
        data = {'name': 'Test'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_new_group_with_login_send_status(self):
        """
        New group with login
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('groups_list_api')
        data = {'name': 'Test', 'status': 'close'}
        response = client.post(url, data, format='json')
        group = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(group['status'], 'open')


class GroupDetailAPITests(SecretSantaTestCase):

    def test_detail_group_check_page_without_login(self):
        """
        Detail group without login
        """
        self.check_page_without_login('groups_detail_api', self.group.id,)

    def test_detail_group_with_login(self):
        """
        Detail group with login
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('groups_detail_api', args=(self.group.id,))
        response = client.get(url)
        group = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(group['name'], 'Test')

    def test_changue_group_with_login(self):
        """
        Changue group name with login
        """
        data = {'name': 'Test2'}
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        group = Group.objects.get(name="Test")
        url = reverse('groups_detail_api', args=(group.id,))
        response = client.put(url, data, format='json')
        group = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(group['name'], 'Test2')

    def test_changue_status_group_with_login(self):
        """
        Changue group status with login
        """
        data = {'status': 'close'}
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('groups_detail_api', args=(self.group.id,))
        response = client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_changue_status_group_with_login_other_user(self):
        """
        Changue group status with login other user
        Because the group is not being the user owner
        """
        data = {'status': 'close'}
        client = APIClient()
        client.login(username=self.user2.username, password=self.user2.username)
        group = Group.objects.get(name="Test")
        url = reverse('groups_detail_api', args=(group.id,))
        response = client.patch(url, data, format='json')
        group = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InscriptionAPITests(SecretSantaTestCase):

    def test_list_inscriptions_check_page_without_login(self):
        """
        List inscriptions without login
        """
        self.check_page_without_login('inscriptions_list_api')

    def test_list_inscriptions_with_login(self):
        """
        List inscriptions with login
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('inscriptions_list_api')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inscriptions = response.json()
        for inscription in inscriptions:
            inscription_user = User.objects.get(pk=inscription['user'])
            self.assertEqual(inscription_user.username, self.user.username)


class InscriptionDetailAPITests(SecretSantaTestCase):

    def test_list_inscriptions_check_page_without_login(self):
        """
        Detail inscription without login
        """
        inscription = Inscription.objects.get(group=self.group, user=self.user)
        self.check_page_without_login('inscriptions_detail_api', inscription.id)

    def test_list_inscriptions_with_login(self):
        """
        Detail inscription with login
        """
        inscription = Inscription.objects.get(group=self.group, user=self.user)
        client = APIClient()
        client.login(username=self.user.username, password=self.user.username)
        url = reverse('inscriptions_detail_api', args=(inscription.id,))
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inscription_response = response.json()
        inscription_user = User.objects.get(pk=inscription_response['user'])
        self.assertEqual(inscription_user.username, self.user.username)

    def test_list_inscriptions_with_login_other_user(self):
        """
        Detail inscription with login other user
        """
        inscription = Inscription.objects.get(group=self.group, user=self.user)
        client = APIClient()
        client.login(username=self.user2.username, password=self.user2.username)
        url = reverse('inscriptions_detail_api', args=(inscription.id,))
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

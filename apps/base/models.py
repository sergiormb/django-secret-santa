# -*- coding: utf-8 -*-
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User as auth_User
from django.db import models
from django.utils.translation import ugettext as _


STATUS_CHOICES = (
    ('open', _('Open')),
    ('moving', _('Moving')),
    ('close', _('Close')),
)


class User(auth_User):

    class Meta:
        proxy = True
        ordering = ('first_name', )


class Group(models.Model):
    creator = models.ForeignKey(
        User, related_name='groups_created', verbose_name=_("Creator"))
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        _('Created date'), auto_now_add=True)
    end_date = models.DateTimeField(
        _('End date'), blank=True, null=True)
    limit_number = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        _('Status'), max_length=10, choices=STATUS_CHOICES,
        default='open', db_index=True)

    @property
    def users(self):
        inscriptions = self.inscriptions.all()
        users = []
        for inscription in inscriptions:
            users.append(inscription.user)
        return users

    def move_bag(self):
        if self.status == 'moving':
            inscriptions = self.inscriptions.all()
            users = self.users
            for inscription in inscriptions:
                secret_user = inscription.user
                while inscription.user == secret_user:
                    secret_user = random.choice(users)
                inscription_secret = Inscription.objects.get(user=secret_user, group=inscription.group)
                inscription.give_gift = inscription_secret
                inscription.save()
                send_mail(
                    'Group %s has closed, prepare your gift' % inscription.group.name,
                    'You must give %s. His interests are %s' % (inscription.give_gift.user, inscription.give_gift.preferences),
                    'secretsantadjango@gmail.com',
                    [inscription.user.email],
                    fail_silently=False,
                )
                users.remove(secret_user)

    def close_group(self):
        if self.status == 'open' and len(self.users) > 2:
            self.status = 'moving'
            self.move_bag()
            self.status = 'close'
            self.save()

    def __unicode__(self):
        return self.name


class Inscription(models.Model):
    user = models.ForeignKey(
        User, related_name='inscriptions', verbose_name=_("User"))
    group = models.ForeignKey(
        Group, related_name='inscriptions', verbose_name=_("Group"))
    preferences = models.CharField(_('Preferences'), max_length=255)
    give_gift = models.OneToOneField(
        'self',
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ('user', 'group',)

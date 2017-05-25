from django.utils.translation import ugettext as _

import django_tables2 as tables

from base.models import Inscription, Group


class InscriptionTable(tables.Table):
    group = tables.LinkColumn(
        verbose_name=_('Group'), viewname='group_detail',
        order_by=('name', ), orderable=False,
        args=(tables.A('group.id'), ))

    class Meta:
        model = Inscription
        fields = ('group', 'preferences')


class InscriptionClosedTable(tables.Table):
    group = tables.LinkColumn(
        verbose_name=_('Group'), viewname='group_detail',
        order_by=('name', ), orderable=False,
        args=(tables.A('group.id'), ))
    give_gift = tables.Column(accessor='give_gift.user')
    preferences = tables.Column(accessor='give_gift.preferences')
    end_date = tables.Column(accessor='group.end_date')

    class Meta:
        model = Inscription
        fields = ('group', 'give_gift', 'preferences')


class GroupTable(tables.Table):
    name = tables.LinkColumn(
        verbose_name=_('Name'), viewname='group_detail',
        order_by=('name', ),
        args=(tables.A('id'), ))

    class Meta:
        model = Group
        fields = ('name', 'end_date', 'limit_number', 'status')

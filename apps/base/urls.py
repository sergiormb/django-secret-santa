"""urlconf for the base application"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from base import views as base_views


urlpatterns = [
    url(r'^$', base_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', base_views.signup, name='signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^inscriptions$', base_views.inscription_list, name='inscription_list'),
    url(r'^group/(?P<pk>[\d]+)/close$', base_views.group_close, name='group_close'),
    url(r'^group/(?P<pk>[\d]+)/inscription$', base_views.InscriptionCreate.as_view(), name='inscription_create'),
    url(r'^group/(?P<pk>[\d]+)/$', base_views.GroupDetailView.as_view(), name='group_detail'),
    url(r'^groups$', base_views.GroupListView.as_view(), name='group_list'),
    url(r'^groups/new/$', base_views.GroupCreateView.as_view(), name='group_create'),

]

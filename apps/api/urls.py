from django.conf.urls import url, include

from api import views


urlpatterns = [
    url(r'^groups/$', views.GroupListAPIView.as_view(), name="groups_list_api"),
    url(r'^groups/(?P<pk>[0-9]+)/$', views.GroupDetailAPIView.as_view(), name="groups_detail_api"),
    url(r'^inscriptions/$', views.InscriptionListAPIView.as_view(), name="inscriptions_list_api"),
    url(r'^inscriptions/(?P<pk>[0-9]+)/$', views.InscriptionDetailAPIView.as_view(), name="inscriptions_detail_api"),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(
        r'^auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from base.models import Group, Inscription

from api import CsrfExemptSessionAuthentication
from api.serializers import GroupSerializer, GroupUpdateSerializer, InscriptionSerializer, InscriptionUpdateSerializer


class GroupListAPIView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'creator', 'status')

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return GroupUpdateSerializer
        return GroupSerializer

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(creator=user)


class GroupDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = GroupSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def check_is_creator(self, request):
        instance = self.get_object()
        status_response = request.data.get('status', None)
        if request.user == instance.creator and len(instance.users) > 2:
            if status_response == 'close':
                instance.close_group()
            return True
        else:
            return False

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return GroupUpdateSerializer
        return GroupSerializer

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(creator=user)

    def patch(self, request, *args, **kwargs):
        status_response = request.data.get('status', None)

        if status_response:
            is_creator = self.check_is_creator(request)
            if not is_creator:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super(GroupDetailAPIView, self).patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        status_response = request.data.get('status', None)

        if status_response:
            is_creator = self.check_is_creator(request)
            if not is_creator:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super(GroupDetailAPIView, self).put(request, *args, **kwargs)


class InscriptionListAPIView(generics.ListCreateAPIView):
    serializer_class = InscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Inscription.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return InscriptionUpdateSerializer
        return InscriptionSerializer


class InscriptionDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = InscriptionSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return InscriptionUpdateSerializer
        return InscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Inscription.objects.filter(user=user)

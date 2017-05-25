from rest_framework import serializers
from base.models import Group, Inscription


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupUpdateSerializer(GroupSerializer):

    def create(self, validated_data):
        creator = self.context['request'].user
        validated_data.update({'creator': creator})
        status = validated_data.get('status', None)
        if status:
            validated_data.pop('status')
        return Group.objects.create(**validated_data)

    class Meta:
        model = Group
        fields = ('name', 'end_date', 'limit_number', 'status')


class InscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inscription
        fields = ('user', 'preferences', 'group')


class InscriptionUpdateSerializer(InscriptionSerializer):

    class Meta:
        model = Inscription
        fields = ('preferences', 'group')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({'user': user})
        return Inscription.objects.create(**validated_data)
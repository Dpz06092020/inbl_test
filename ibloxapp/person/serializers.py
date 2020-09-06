from rest_framework import serializers
from person.models import Person


class FetchPersonSerializer(serializers.ModelSerializer):

    enabled = serializers.SerializerMethodField('get_enabled_from_data')
    guid = serializers.SerializerMethodField('get_guid_from_data')

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'city', 'enabled', 'guid']

    def get_enabled_from_data(self, person):
        enabled = person.data.enabled
        return enabled

    def get_guid_from_data(self, person):
        guid = person.data.guid
        return guid

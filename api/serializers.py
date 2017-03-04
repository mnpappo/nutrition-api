from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import MyPhoto

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyPhoto
        fields = '__all__'

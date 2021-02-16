from rest_framework import serializers
from .models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend

class UserSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'password', 'profile_img', 'followers', 'name']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data, partial=True):
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)

        instance.save()
        return instance

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')


        attrs['user'] = user
        return attrs
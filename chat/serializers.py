from rest_framework import serializers
from .models import Room, Message
from account.models import User

class GetUserMixin:
    def get_user_from_request(self):
        request = self.context.get('request')
        if not request:
            return None
        if not hasattr(request, 'user'):
            return None
        return request.user

class ParticipantsField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return User.objects.get(username=value)

class RoomSerializer(GetUserMixin, serializers.ModelSerializer):
    participants = ParticipantsField(many=True)
    class Meta:
        model = Room
        fields = ['id', 'title', 'participants', 'description']

    def validate_participants(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if user not in value:
            raise serializers.ValidationError('User must be in participants.')
        return value

class MessageSerializer(GetUserMixin, serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'content', 'sender', 'timestamp']

    def validate_sender(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if user.id != value.id:
            raise serializers.ValidationError('User must be same with sender.')
        return value

    def validate_room(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if not user.room_set.filter(id=value.id):
            raise serializers.ValidationError('User must be in room.')

        url_room_pk = self.context.get('view').kwargs.get('parent_lookup_room')
        if int(url_room_pk) != value.id:
            raise serializers.ValidationError('Room must be same with room of url.')
        return value
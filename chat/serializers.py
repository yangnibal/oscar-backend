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

class ParticipantsField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        user = User.objects.get(username=value)
        serializer = UserSerializer(user)
        if serializer.is_valid():
            return serializer.data
        return

class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'profile_img']

    def to_internal_value(self, value):
        user = User.objects.get(id=value)
        serializer = UserSerializer(user)
        if serializer.is_valid():
            return serializer.data
        return

class RoomSerializer(GetUserMixin, serializers.ModelSerializer):
    participants = ParticipantsSerializer(many=True)
    last_message = MessageSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'title', 'participants', 'description', 'last_message']

    def validate_participants(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if user not in value:
            raise serializers.ValidationError('User must be in participants.')
        return value


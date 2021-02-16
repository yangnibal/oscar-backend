from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from account.models import User
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response

class RoomViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        return user.room_set.all()

    @action(detail=False, list=True, methods=['GET'])
    def my(self, request):
        user = request.user
        serializer = RoomSerializer(user.room_set.all(), many=True)
        return Response(serializer.data)
    
class MessageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        parents_query_dict = self.get_parents_query_dict()
        room_id = parents_query_dict.get('room')
        user = self.request.user
        if not user.room_set.filter(id=room_id):
            raise Http404

        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query and self.action == 'list':
            queryset = queryset.filter(content__icontains=query)
        return queryset
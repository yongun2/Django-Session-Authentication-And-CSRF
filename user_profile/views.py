from operator import itemgetter

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileView(APIView):
    def get(self, request):
        user = self.request.user
        username = user.username

        user = User.objects.get(id=user.id)

        user_profile = UserProfile.objects.get(user_id=user.id)
        user_profile = UserProfileSerializer(user_profile)

        return Response(data={'profile': user_profile.data, 'username': str(username)}, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.request.user
        username = user.username

        data = self.request.data
        name, phone, nickname = itemgetter('name', 'phone', 'nickname')(data)

        user = User.objects.get(id=user.id)

        UserProfile.objects.filter(user_id=user.id).update(name=name, phone=phone, nickname=nickname)

        user_profile = UserProfile.objects.get(user_id=user.id)
        user_profile = UserProfileSerializer(user_profile)

        return Response(data={'profile': user_profile.data, 'username': str(username)}, status=status.HTTP_200_OK)

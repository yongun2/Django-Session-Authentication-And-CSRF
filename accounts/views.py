from operator import itemgetter

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import UserProfile


@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data

        username, password, name, phone, nickname = \
            itemgetter('username', 'password', 'name', 'phone', 'nickname')(data)

        if User.objects.filter(username=username).exists():
            return Response({'error': "username already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        user = User.objects.get(username=username)
        user_profile = UserProfile(user=user, name=name, phone=phone, nickname=nickname)
        user_profile.save()

        return Response(data={"username": username, "name": name, "phone": phone, "nickname": nickname},
                        status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
class CheckDuplicateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        username = data['username']

        if User.objects.filter(username=username).exists():
            return Response(data={"username": username}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(data={"username": username}, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'success': 'CSRF cookie set'}, status=status.HTTP_200_OK)

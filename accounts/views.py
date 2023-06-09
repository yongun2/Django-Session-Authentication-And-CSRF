from operator import itemgetter

from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.models import UserProfile
from .serializers import UserSerializer


class CheckAuthenticatedView(APIView):
    def get(self, request):
        try:
            isAuthenticated = User.is_authenticated

            if isAuthenticated:
                return Response(data={"isAuthenticated": "true"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"isAuthenticated": "false"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(data={"error": "Something went wrong when checking authentication status"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class AccountsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(data=users.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.request.data

        username, password, name, phone, nickname = \
            itemgetter('username', 'password', 'name', 'phone', 'nickname')(data)

        if User.objects.filter(username=username).exists():
            return Response({'error': "username already exists"}, status=status.HTTP_409_CONFLICT)

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            user = User.objects.get(username=username)
            user_profile = UserProfile(user=user, name=name, phone=phone, nickname=nickname)
            user_profile.save()

            return Response(data={"username": username, "name": name, "phone": phone, "nickname": nickname},
                            status=status.HTTP_201_CREATED)
        except:
            return Response(data={"error": "Something went wrong while registering "},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        user = self.request.user

        user = User.objects.filter(id=user.id).delete()

        return Response(data={"success": "user has deleted"}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class CheckDuplicateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']

        if User.objects.filter(username=username).exists():
            return Response(data={"username": username}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(data={"username": username}, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data

        username, password = itemgetter('username', 'password')(data)

        try:

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response(data={"username": username}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"error": "Something went wrong when login"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    def post(self, request):
        try:
            auth.logout(request)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'error': 'something went wrong when logging out'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'success': 'CSRF cookie set'}, status=status.HTTP_200_OK)

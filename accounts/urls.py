from django.urls import path

from accounts.views import SignupView, GetCSRFToken, CheckDuplicateView, CheckAuthenticatedView, LoginView, LogoutView

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('duplicate', CheckDuplicateView.as_view()),
    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
]
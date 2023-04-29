from django.urls import path

from accounts.views import SignupView, GetCSRFToken, CheckDuplicateView

urlpatterns = [
    path('duplicate', CheckDuplicateView.as_view()),
    path('register', SignupView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
]
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from user_profiles.views import RegisterView
app_name = 'user_profiles'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='register.html',
                                           success_url=reverse_lazy('festival_app:application-create')),
         name='register'),
]

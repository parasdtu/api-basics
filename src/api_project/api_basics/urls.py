from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user/', views.UserListMixin.as_view()),
    path('user/<int:pk>/', views.UserDetailMixin.as_view()),
    path('register/', views.user_reg_view, name="register"),
    path('login/', obtain_auth_token, name="login"),

]

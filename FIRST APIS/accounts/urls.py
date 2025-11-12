from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views, api_views

urlpatterns = [
    # Template URLs
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # API URLs
    path('api/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/user/', api_views.UserDetailAPIView.as_view(), name='api_user_detail'),
    path('api/user/update/', api_views.UpdateUserAPIView.as_view(), name='api_user_update'),
    path('api/change-password/', api_views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/protected/', api_views.ProtectedDataAPIView.as_view(), name='api_protected'),
    
    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
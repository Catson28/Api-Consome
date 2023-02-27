from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,
    ProtectedView,
    HasRoleView,
    HasPermissionView,
    UpdateUserView,
    LogoutView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('has_role/<str:role>/', HasRoleView.as_view(), name='has_role'),
    path('has_permission/<str:permission>/', HasPermissionView.as_view(), name='has_permission'),
    path('update_user/', UpdateUserView.as_view(), name='update_user'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
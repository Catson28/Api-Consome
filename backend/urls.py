from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include("backend.authentication.urls")),
    path('chat/', include("backend.chat.urls")),
]

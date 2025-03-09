from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('line_app/', include('line_app.urls')),
    path('toilet/', include('toilet.urls')),
]

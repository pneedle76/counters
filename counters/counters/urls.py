from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('days_until_christmas/', include('days_until_christmas.urls')),
    path('admin/', admin.site.urls),
]

"""
DEPRECATED: URL patterns moved to app.api.urls
Kept for backward compatibility if another module includes('app.urls').
"""
from django.urls import include, path

app_name = 'app'

urlpatterns = [
    path('', include('app.api.urls')),
]

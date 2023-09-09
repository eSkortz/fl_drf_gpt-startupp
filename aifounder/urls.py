from django.urls import path, include

urlpatterns = [
    path('django_jain/', include('fundraising.urls')),
    path('django_jain/', include('swagger')),
]
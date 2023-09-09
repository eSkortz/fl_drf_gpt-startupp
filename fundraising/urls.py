from django.urls import path
from . import views

urlpatterns = [
    path('gpt-35/', views.MyView.gpt_35, name='gpt-35'),
    path('gpt-35-16/', views.MyView.gpt_35_16, name='gpt-35-16'),
    path('gpt-4/', views.MyView.gpt_4, name='gpt-4'),
    path('gpt-4-32/', views.MyView.gpt_4_32, name='gpt-4-32'),
]
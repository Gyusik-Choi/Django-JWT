from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create_review/', views.create_review, name='create_review'),
]
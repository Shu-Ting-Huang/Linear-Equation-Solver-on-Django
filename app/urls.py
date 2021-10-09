from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('simple_row_ops',views.simple_row_ops),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('row_ops_iframe',views.row_ops_iframe),
]
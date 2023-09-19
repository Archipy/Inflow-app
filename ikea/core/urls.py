
from django.contrib import admin
from django.urls import path
from .views import IndexView,IndexNoches

urlpatterns = [
    path('', IndexView.as_view() , name='index'),
    path('index_noches/', IndexNoches.as_view() , name='index_noches'),
]

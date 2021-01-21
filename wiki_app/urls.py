from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home_page', views.home_page_render),
    path('register_page', views.register_page_render)
]
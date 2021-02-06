from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('back', views.back),
    path('log_in', views.log_in_page_render),
    path('home_page', views.home_page_render),
    path('register_page', views.register_page_render),
    path('user_profile_page/<int:user_id>', views.user_profile_page),
    path('add_entry_page', views.add_entry_page),
    path('deities_by_religion/<str:deity_religion>', views.deities_by_religion_page),
    path('deities_by_location/<str:deity_location>', views.deities_by_location_page),
    path('deity_info_page/<int:deity_id>', views.deity_info_page),
    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login),
    path('searchbar', views.searchbar),
    path('add_deity', views.add_deity),
    path('deity_edit_page/<int:deity_id>', views.deity_edit_page),
    path('edit_deity/<int:deity_id>', views.edit_deity),
]
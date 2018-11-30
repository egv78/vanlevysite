from django.urls import path, re_path

from . import views


app_name = 'vanlevy'

urlpatterns = [
    path('', views.vl_home_view, name='home'),
    path('home/', views.vl_home_view, name='home'),
    path('about/', views.vl_about_view, name='about'),
    path('resources/', views.vl_resources_view, name='resources'),
    path('cool-stuff/', views.vl_cool_stuff_view, name='cool_stuff')

]


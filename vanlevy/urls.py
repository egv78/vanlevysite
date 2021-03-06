from django.urls import path, re_path
from django.conf.urls import handler404

from . import views


app_name = 'vanlevy'

urlpatterns = [
    path('', views.vl_home_view, name='blank'),
    path('home/', views.vl_home_view, name='home'),
    path('about/', views.vl_about_view, name='vl_about'),
    path('resources/', views.vl_resources_view, name='resources'),
    path('cool-stuff/', views.vl_cool_stuff_view, name='cool_stuff'),
    path('dice-rollers/', views.vl_dice_rollers_view, name='dice_rollers'),
    path('portal/', views.personal_portal, name='portal'),
    path('terms/', views.vl_terms_view, name='terms'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('404/', views.vl_error, name='404'),
    path('kobolds/', views.kobolds_about_view, name='kobolds_about'),
    path('kobolds/terms/', views.kobolds_terms_view, name='kobolds_terms'),
    path('kobolds/privacy/', views.kobolds_privacy_view, name='kobolds_privacy'),
]

handler404 = views.vl_error

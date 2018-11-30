from django.urls import path, re_path

from . import views

app_name = 'swdice'


urlpatterns = [
    path('', views.about, name='about'),
    path('dockingbay/', views.DockingBay.as_view(template_name="swdice/dockingbay.html"), name='dockingbay'),
    path('room/<int:swroom_id>/', views.ViewRoom.as_view(), name='swroom'),
    path('makeroom/', views.make_sw_room, name='makeroom'),
    path('enter_with_passcode/', views.DockingBay.as_view(template_name="swdice/enter_with_passcode.html"),
         name='enter_passcode'),
]


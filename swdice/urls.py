from django.urls import path, re_path

from . import views

app_name = 'swdice'


urlpatterns = [
    path('', views.about, name='about'),
    path('dockingbay/', views.DockingBay.as_view(template_name="swdice/dockingbay.html"), name='dockingbay'),
    path('room/<int:swroom_id>/', views.ViewRoom.as_view(), name='swroom'),
    path('room/<int:swroom_id>/info', views.RoomInfo.as_view(), name='swroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>', views.RoomPlayerInfo.as_view(), name='swroom_player_info'),
    path('makeroom/', views.make_sw_room, name='makeroom'),
    path('enter_with_passcode/', views.DockingBay.as_view(template_name="swdice/enter_with_passcode.html"),
         name='enter_passcode'),
    path('switch_avatar/', views.DockingBay.as_view(template_name="swdice/switch_avatar.html"),
         name='switch_avatar'),
    path('switch_avatar/room/<int:swroom_id>/', views.DockingBay.as_view(template_name="swdice/switch_avatar.html"),
         name='switch_avatar_room'),
]


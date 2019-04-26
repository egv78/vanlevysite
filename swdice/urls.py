from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

app_name = 'swdice'


urlpatterns = [
    path('', views.about, name='about'),

    path('bad_room',
         views.BadRoom.as_view(template_name="swdice/bad_room.html"), name='bad_room'),

    path('enter_with_passcode/',
         views.HubView.as_view(template_name="swdice/enter_with_passcode.html"), name='enter_passcode'),
    path('enter_with_passcode/<int:swroom_id>/',
         views.HubView.as_view(template_name="swdice/enter_with_passcode.html"), name='enter_passcode_room'),
    path('dockingbay/',
         views.HubView.as_view(template_name="swdice/hub_dockingbay.html"), name='dockingbay'),
    path('switch_avatar/',
         views.HubView.as_view(template_name="swdice/switch_avatar.html"), name='switch_avatar'),
    path('switch_avatar/room/<int:swroom_id>/',
         views.HubView.as_view(template_name="swdice/switch_avatar.html"), name='switch_avatar_room'),

    path('room/<int:swroom_id>/',
         views.SWRoomViews.as_view(template_name="swdice/room_sw.html"), name='swroom'),
    path('room/<int:swroom_id>/info',
         views.SWRoomViews.as_view(template_name="swdice/room_sw_info.html"), name='swroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.SWRoomViews.as_view(template_name="swdice/room_sw_info_player.html"), name='swroom_player_info'),

    path('room/<int:swroom_id>/direct/<slug:slug>',
         views.DirectLink.as_view(template_name="swdice/room_sw_link_direct"), name='room_sw_link_direct'),

    path('makeroom/',
         views.MakeDiceRoom.as_view(template_name='swdice/room_sw_make.html'), name='make_swroom'),
    path('change_passcode/<int:swroom_id>/',
         views.MakeDiceRoom.as_view(template_name='swdice/room_sw_passcode_change.html'), name='change_passcode'),

    path('404', views.error, name='404'),
]

handler404 = views.error

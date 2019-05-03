from django.urls import path, re_path
from django.conf.urls import handler404

from . import views
from swdice import views as sw_views

app_name = 'myzdice'


urlpatterns = [
    path('', views.about, name='about'),

    path('bad_room',
         sw_views.BadRoom.as_view(template_name="myzdice/bad_room.html"), name='bad_room'),

    path('enter_with_passcode/',
         sw_views.HubView.as_view(template_name="myzdice/enter_with_passcode.html"), name='enter_passcode'),
    path('enter_with_passcode/<int:swroom_id>/',
         sw_views.HubView.as_view(template_name="myzdice/enter_with_passcode.html"), name='enter_passcode_room'),
    path('the_zone/',
         sw_views.HubView.as_view(template_name="myzdice/hub_the_zone.html"), name='the_zone'),
    path('switch_avatar/',
         sw_views.HubView.as_view(template_name="myzdice/replace_avatar.html"), name='switch_avatar'),
    path('switch_avatar/room/<int:swroom_id>/',
         sw_views.HubView.as_view(template_name="myzdice/replace_avatar.html"), name='switch_avatar_room'),

    path('room/<int:swroom_id>/',
         views.MYZRoomViews.as_view(template_name="myzdice/room_myz.html"), name='myzroom'),
    path('room/<int:swroom_id>/info',
         views.MYZRoomViews.as_view(template_name="myzdice/room_myz_info.html"), name='myzroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.MYZRoomViews.as_view(template_name="myzdice/room_myz_info_player.html"), name='myzroom_player_info'),

    path('room/<int:swroom_id>/direct/<slug:slug>',
         sw_views.DirectLink.as_view(template_name="myzdice/room_myz_link_direct"), name='room_myz_link_direct'),

    path('makeroom/',
         sw_views.MakeDiceRoom.as_view(template_name='myzdice/room_myz_make.html'), name='make_myzroom'),
    path('change_passcode/<int:swroom_id>/',
         sw_views.MakeDiceRoom.as_view(template_name='myzdice/room_myz_passcode_change.html'), name='change_passcode'),

    path('404', views.error, name='404'),
]

handler404 = views.error

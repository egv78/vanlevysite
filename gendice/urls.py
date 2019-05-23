from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

app_name = 'gendice'


urlpatterns = [
    path('', views.about, name='about'),

    path('bad_room',
         views.BadRoom.as_view(template_name="gendice/bad_room_gen.html"), name='bad_room'),

    path('enter_with_passcode/',
         views.HubView.as_view(template_name="gendice/enter_with_passcode_gen.html"), name='enter_passcode_gen'),
    path('enter_with_passcode/<int:swroom_id>/',
         views.HubView.as_view(template_name="gendice/enter_with_passcode_gen.html"), name='enter_passcode_room'),
    path('confluence/',
         views.HubView.as_view(template_name="gendice/hub_confluence.html"), name='confluence'),
    path('switch_avatar/room/<int:swroom_id>/',
         views.HubView.as_view(template_name="gendice/replace_avatar_gen.html"), name='switch_avatar_room_gen'),

    path('room/<int:swroom_id>/',
         views.SWRoomViews.as_view(template_name="gendice/room_gen.html"), name='genroom'),
    path('room/<int:swroom_id>/info',
         views.SWRoomViews.as_view(template_name="gendice/room_gen_info.html"), name='genroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.SWRoomViews.as_view(template_name="gendice/room_gen_info_player.html"), name='genroom_player_info'),

    path('room_nc/<int:swroom_id>/',
         views.SWRoomViews.as_view(template_name="gendice/room_gen_nc.html"), name='genroom_nc'),

    path('room/<int:swroom_id>/direct/<slug:slug>',
         views.DirectLink.as_view(template_name="swdice/room_gen_link_direct"), name='room_gen_link_direct'),

    path('makeroom/',
         views.MakeDiceRoom.as_view(template_name='gendice/room_gen_make.html'), name='make_genroom'),
    path('change_passcode/<int:swroom_id>/',
         views.MakeDiceRoom.as_view(template_name='gendice/room_gen_passcode_change.html'), name='change_passcode_gen'),

    path('404', views.error_gen, name='404'),
]

handler404 = views.error_gen

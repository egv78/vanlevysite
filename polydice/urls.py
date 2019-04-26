from django.urls import path, re_path
from django.conf.urls import handler404

from . import views
from swdice import views as sw_views

app_name = 'polydice'


urlpatterns = [
    path('', views.about, name='about'),

    path('bad_room',
         sw_views.BadRoom.as_view(template_name="polydice/bad_room_poly.html"), name='bad_room'),

    path('enter_with_passcode/',
         sw_views.HubView.as_view(template_name="polydice/enter_with_passcode_poly.html"), name='enter_passcode'),
    path('enter_with_passcode/<int:swroom_id>/',
         sw_views.HubView.as_view(template_name="polydice/enter_with_passcode_poly.html"), name='enter_passcode_room'),
    path('dungeon/',
         sw_views.HubView.as_view(template_name="polydice/hub_dungeon.html"), name='dungeon'),
    path('switch_avatar/',
         sw_views.HubView.as_view(template_name="polydice/replace_avatar_poly.html"), name='switch_avatar'),
    path('switch_avatar/room/<int:swroom_id>/',
         sw_views.HubView.as_view(template_name="polydice/replace_avatar_poly.html"), name='switch_avatar_room'),

    path('room/<int:swroom_id>/',
         views.PolyRoomViews.as_view(template_name="polydice/room_poly.html"), name='polyroom'),
    path('room/<int:swroom_id>/info',
         views.PolyRoomViews.as_view(template_name="polydice/room_poly_info.html"), name='polyroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.PolyRoomViews.as_view(template_name="polydice/room_poly_info_player.html"), name='polyroom_player_info'),

    path('room/<int:swroom_id>/direct/<slug:slug>',
         sw_views.DirectLink.as_view(template_name="swdice/room_poly_link_direct"), name='room_poly_link_direct'),

    path('makeroom/',
         sw_views.MakeDiceRoom.as_view(template_name='polydice/room_poly_make.html'), name='make_polyroom'),
    path('change_passcode/<int:swroom_id>/',
         sw_views.MakeDiceRoom.as_view(template_name='polydice/room_poly_passcode_change.html'), name='change_passcode'),

    path('404', views.error, name='404'),
]

handler404 = views.error

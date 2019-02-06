from django.urls import path, re_path

from . import views

app_name = 'swdice'


urlpatterns = [
    path('', views.about, name='about'),
    path('dockingbay/', views.DockingBay.as_view(template_name="swdice/dockingbay.html"), name='dockingbay'),
    path('room/<int:swroom_id>/',
         views.SWRoomViews.as_view(template_name="swdice/swroom.html"), name='swroom'),
    path('room/<int:swroom_id>/info',
         views.SWRoomViews.as_view(template_name="swdice/swroom_info.html"), name='swroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.SWRoomViews.as_view(template_name="swdice/swroom_player_info.html"), name='swroom_player_info'),
    path('makeroom/', views.make_sw_room, name='makeroom'),
    path('enter_with_passcode/', views.DockingBay.as_view(template_name="swdice/enter_with_passcode.html"),
         name='enter_passcode'),
    path('switch_avatar/', views.DockingBay.as_view(template_name="swdice/switch_avatar.html"),
         name='switch_avatar'),
    path('switch_avatar/room/<int:swroom_id>/', views.DockingBay.as_view(template_name="swdice/switch_avatar.html"),
         name='switch_avatar_room'),
]

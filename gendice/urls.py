from django.urls import path, re_path

from . import views

app_name = 'gendice'


urlpatterns = [
    path('', views.about, name='about'),
    path('confluence/', views.DockingBay.as_view(template_name="gendice/confluence.html"), name='confluence'),
    path('makeroom/', views.MakeSWRoom.as_view(template_name='gendice/make_genroom.html'), name='make_genroom'),
    path('room/<int:swroom_id>/',
         views.SWRoomViews.as_view(template_name="gendice/genroom.html"), name='genroom'),
    path('room/<int:swroom_id>/info',
         views.SWRoomViews.as_view(template_name="gendice/genroom_info.html"), name='genroom_info'),
    path('room/<int:swroom_id>/player-info/<int:player_id>',
         views.SWRoomViews.as_view(template_name="gendice/genroom_player_info.html"), name='genroom_player_info'),
    path('room/<int:swroom_id>/direct/<slug:slug>', views.direct_view_gen, name='genroom_direct'),
    path('switch_avatar/room/<int:swroom_id>/', views.DockingBay.as_view(template_name="gendice/switch_avatar_gen.html"),
         name='switch_avatar_room_gen'),
    path('enter_with_passcode/', views.DockingBay.as_view(template_name="gendice/enter_with_passcode_gen.html"),
         name='enter_passcode_gen'),
]

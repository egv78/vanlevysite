from django.contrib import admin
from swdice.models import SWRoom, SWRoomToUser


class SWRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'created_by', 'is_open')

    def created_on(self, swroom_object):
        return swroom_object.created_on

    def created_by(self, swroom_object):
        return swroom_object.created_by

    def is_open(self, swroom_object):
        return swroom_object.open_to_all == True
    is_open.boolean = True


class SWRoomToUserAdmin(admin.ModelAdmin):
    list_display = ('user_col', 'avatar_col', 'room_col', 'game_master', 'banned')

    def user_col(self, user_object):
        return user_object.user_id
    user_col.admin_order_field = 'user_id'
    user_col.short_description = 'User'

    def avatar_col(self, avatar_object):
        return avatar_object.avatar_id
    avatar_col.admin_order_field = 'avatar_id'
    avatar_col.short_description = 'Avatar'

    def room_col(self, room_object):
        return room_object.room_id
    room_col.admin_order_field = 'room_id'
    room_col.short_description = 'Room'


admin.site.register(SWRoom, SWRoomAdmin)
admin.site.register(SWRoomToUser, SWRoomToUserAdmin)

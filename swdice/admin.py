from django.contrib import admin
from swdice.models import SWRoom, SWRoomToUser


class SWRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'created_on', 'created_by', 'is_open', 'genesys')

    def room_name(self, swroom_object):
        if len(swroom_object.name) < 55:
            return swroom_object.name
        else:
            return swroom_object.name[:50] + "..."

    room_name.admin_order_field = 'room_id'
    room_name.short_description = 'Room'

    def created_on(self, swroom_object):
        return swroom_object.created_on

    def created_by(self, swroom_object):
        return swroom_object.created_by

    def is_open(self, swroom_object):
        return swroom_object.open_to_all is True
    is_open.boolean = True

    def genesys(self, swroom_object):
        return swroom_object.genesys is True
    genesys.boolean = True


class SWRoomToUserAdmin(admin.ModelAdmin):
    list_display = ('user_col', 'avatar_col', 'room_col', 'game_master', 'banned')

    def user_col(self, room_to_user_object):
        return room_to_user_object.user_id
    user_col.admin_order_field = 'user_id'
    user_col.short_description = 'User'

    def avatar_col(self, room_to_user_object):
        if room_to_user_object.avatar_id is None:
            return room_to_user_object.avatar_id
        elif len(room_to_user_object.avatar_id.avatar_name) < 35:
            return room_to_user_object.avatar_id
        else:
            return room_to_user_object.avatar_id.avatar_name[:30] + "..."

    avatar_col.admin_order_field = 'avatar_id'
    avatar_col.short_description = 'Avatar'

    def room_col(self, room_to_user_object):
        if len(room_to_user_object.room_id.name) < 55:
            return room_to_user_object.room_id.name
        else:
            return room_to_user_object.room_id.name[:50] + "..."
    room_col.admin_order_field = 'room_id'
    room_col.short_description = 'Room'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('room_id', 'user_id')
        return self.readonly_fields


admin.site.register(SWRoom, SWRoomAdmin)
admin.site.register(SWRoomToUser, SWRoomToUserAdmin)

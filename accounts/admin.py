# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as lazy
from accounts.models import UserProfile, VanLevyUser, Avatar


@admin.register(VanLevyUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (lazy('Personal info'), {'fields': ('first_name', 'last_name')}),
        (lazy('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff')  # 'first_name', 'last_name',
    search_fields = ('email', 'username')  # 'first_name', 'last_name',
    ordering = ('email', 'username')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'description', 'has_image')
    search_fields = ('user', 'first_name', 'last_name')
    # ordering = ('user', 'first_name', 'last_name')

    def first_name(self, profile_object):
        return profile_object.user_first_name
    first_name.admin_order_field = 'user_first_name'
    first_name.short_description = 'first name'

    def last_name(self, profile_object):
        return profile_object.user_last_name
    last_name.admin_order_field = 'user_last_name'
    last_name.short_description = 'last name'

    def bio(self, profile_object):
        return profile_object.user_bio

    def description(self, profile_object):
        return profile_object.user_description

    def has_image(self, profile_object):
        if profile_object.user_image:
            return True
        else:
            return False
    has_image.boolean = True


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'description', 'has_image', 'is_deleted')
    list_display_links = ('avatar', )

    def avatar(self, avatar_object):
        return avatar_object.avatar_name

    def description(self, avatar_object):
        return avatar_object.avatar_description

    def has_image(self, avatar_object):
        if avatar_object.avatar_image:
            return True
        else:
            return False
    has_image.boolean = True

    def is_deleted(self, avatar_object):
        return avatar_object.deleted == True
    is_deleted.boolean = True


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Avatar, AvatarAdmin)

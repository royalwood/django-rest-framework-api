from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (User, NonMember, BlockedUser, UserProfileDetail, VerificationCode, UserProfileCategory)
from .forms import UserCreationForm, UserChangeForm


class UCROOUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("email", "name", "is_staff",)
    list_filter = ("is_staff", "is_active",)
    search_fields = ("email", "name", "uni", "campus", "course", "groups",)
    filter_horizontal = ("groups", "user_permissions",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("name", "password")}),
        ("Institution info", {"fields": ("uni", "campus", "course", "school", "groups",)}),
        ("Contact info", {"fields": ("email", "email_secondary", "preferred_email",)}),
        ("Personal info", {"fields": ("first_name", "last_name", "gender", "profile_pic", "banner_pic", "vet_id",
                                      "facebook_id", "csu_id", "signup_source",)}),
        ("User meta", {"fields": ("iphone_version", "ios_apn_token", "android_version", "auth_token_mobile",
                                  "android_gcm", "count_profile_views",
                                  "start_year", "year_of_completion", )}),
        ("User transactions", {"fields": ("on_campus", "read_anonymity", "finished", "international", "is_vet",
                                          "is_signed_flg", "latitude", "longitude", "state")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
        ("Account Settings", {"fields": ("email_notifications",)}),
    )


admin.site.register(User, UCROOUserAdmin)
# misc models registered below
admin.site.register(NonMember)
admin.site.register(BlockedUser)
admin.site.register(UserProfileCategory)
admin.site.register(UserProfileDetail)
admin.site.register(VerificationCode)

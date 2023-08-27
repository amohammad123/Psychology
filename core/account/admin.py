from django.contrib import admin
from account.models import user, profile


class CustomUserAdmin(admin.ModelAdmin):
    model = user.CustomUser
    list_display = ['id', 'username', 'type', 'is_superuser', 'is_verified']
    list_filter = ['is_superuser', 'is_verified', 'type']
    ordering = ("create_date",)
    fieldsets = (
        ("authentication", {"fields": ("username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


class CustomClientAdmin(admin.ModelAdmin):
    model = profile.Client
    list_display = ['id', 'first_name', 'last_name']
    ordering = ("create_date",)


class CustomTrappistAdmin(admin.ModelAdmin):
    model = profile.Trappist
    list_display = ['id', 'first_name', 'last_name']
    ordering = ("create_date",)


admin.site.register(user.CustomUser, CustomUserAdmin)
admin.site.register(profile.Client, CustomClientAdmin)
admin.site.register(profile.Trappist, CustomTrappistAdmin)
admin.site.register(user.PhoneCode)

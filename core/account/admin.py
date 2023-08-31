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





admin.site.register(user.CustomUser, CustomUserAdmin)
admin.site.register(user.PhoneCode)
admin.site.register(profile.Profile)
admin.site.register(profile.TrappistRate)
admin.site.register(profile.MedicalDocument)
admin.site.register(profile.SpecializedDocuments)
admin.site.register(profile.DocumentField)
admin.site.register(profile.Notification)
admin.site.register(profile.NotificationFields)

# admin.site.register(profile.Client, CustomClientAdmin)
# admin.site.register(profile.Trappist, CustomTrappistAdmin)
# admin.site.register(profile.Document)
# admin.site.register(profile.DocumentField)

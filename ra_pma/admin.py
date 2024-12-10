from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin  # Import the admin module
from .models import UserProfile  # Import your UserProfile model


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register the User model with the new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Publication

# Register your models here.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    pass


admin.site.register(User, UserAdmin)


class PublicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Publication, PublicationAdmin)
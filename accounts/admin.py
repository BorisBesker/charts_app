from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(ImportExportModelAdmin):
    pass

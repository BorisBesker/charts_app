# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Location, SaveLocation


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    pass


@admin.register(SaveLocation)
class LocationAdmin(ImportExportModelAdmin):
    pass

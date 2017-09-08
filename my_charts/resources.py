from import_export import resources

from .models import Location


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location

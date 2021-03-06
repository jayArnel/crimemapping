'''
    Admin configuration for the Crime module
'''

from django.contrib import admin

import models


class CriminalRecordAdmin(admin.ModelAdmin):
    ''' display CriminalRecord Model in admin page '''
    list_display = (
        'primary_type', 'crime_description', 'location_description', 'date',
        'latitude', 'longitude')
    search_fields = (
        'primary_type', 'crime_description', 'location_description', 'date',
        'latitude', 'longitude')
    list_filter = ('date',)
    date_hierarchy = 'date'

admin.site.register(models.CriminalRecord, CriminalRecordAdmin)

from django.contrib import admin

from backend.models import InstrumentMaster, InstrumentMasterAdmin

admin.site.register(InstrumentMaster, InstrumentMasterAdmin)

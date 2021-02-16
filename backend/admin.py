from django.contrib import admin

from backend.models import InstrumentMaster, InstrumentMasterAdmin, IndexConstituent, IndexConstituentAdmin

admin.site.register(InstrumentMaster, InstrumentMasterAdmin)
admin.site.register(IndexConstituent, IndexConstituentAdmin)

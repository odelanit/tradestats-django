import csv
import io

from django import forms
from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.urls import path
from django_admin_listfilter_dropdown.filters import DropdownFilter


class InstrumentMaster(models.Model):
    exchange_segment = models.CharField(max_length=255, blank=True, null=True)
    exchange_instrument_id = models.BigIntegerField(primary_key=True)
    instrument_type = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    series = models.CharField(max_length=255)
    name_with_series = models.CharField(max_length=255, blank=True, null=True)
    instrument_id = models.BigIntegerField(unique=True)
    price_band_high = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    price_band_low = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    freeze_qty = models.BigIntegerField(blank=True, null=True)
    tick_size = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    lot_size = models.IntegerField(blank=True, null=True)
    underlying_instrument_id = models.BigIntegerField(blank=True, null=True)
    underlying_index_name = models.CharField(max_length=255, blank=True, null=True)
    contract_expiration = models.DateField(blank=True, null=True)
    strike_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    option_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instrument_masters'
        unique_together = (
            ('exchange_instrument_id', 'instrument_type', 'name', 'description', 'series', 'instrument_id'),)


class InstrumentMasterAdmin(admin.ModelAdmin):
    list_display = (
        'instrument_id',
        'exchange_segment',
        'exchange_instrument_id',
        'instrument_type',
        'name',
        'series',
        'description',
        'price_band_high',
        'price_band_low',
        'freeze_qty',
        'tick_size',
        'lot_size',
        'underlying_instrument_id',
        'underlying_index_name',
        'contract_expiration',
        'strike_price',
        'option_type'
    )
    list_filter = (
        ('exchange_segment', DropdownFilter),
        ('instrument_type', DropdownFilter),
        ('series', DropdownFilter)
    )
    search_fields = [
        'instrument_id',
        'exchange_instrument_id',
        'name',
        'description'
    ]


class IndexConstituent(models.Model):
    symbol = models.CharField(max_length=255)
    index = models.CharField(primary_key=True, max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    weightage = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'index_constituents'
        unique_together = (('index', 'symbol', 'company_name', 'sector'),)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': "text/csv,.csv"}))


class IndexConstituentAdmin(admin.ModelAdmin):
    change_list_template = "admin/entities/index_constituent_changelist.html"
    list_display = (
        'index',
        'symbol',
        'company_name',
        'sector',
        'weightage',
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            reader = csv.reader(io_string)

            for row in reader:
                print(row)
                try:
                    ic = IndexConstituent.objects.get(symbol=row[1], index=row[0])
                    ic.company_name = row[2] if row[2] else None
                    ic.sector = row[3] if row[3] else None
                    ic.weightage = row[4] if row[4] else None
                    ic.save()
                except IndexConstituent.DoesNotExist:
                    ic = IndexConstituent.objects.create(
                        index=row[0],
                        symbol=row[1],
                        company_name=row[2] if row[2] else None,
                        sector=row[3] if row[3] else None,
                        weightage=row[4] if row[4] else None
                    )

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")

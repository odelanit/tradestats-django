import json
import os

import psycopg2
import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Fetch instrument/contract masters"

    def handle(self, *args, **options):
        response = requests.post('https://ttblaze.iifl.com/apimarketdata/auth/login', data={
            'secretKey': 'Sffp502@P0',
            'appKey': 'b30ec8206bc86949584481',
            "source": "WebAPI"
        })
        data = response.json()
        token = data['result']['token']

        response = requests.post('https://ttblaze.iifl.com/apimarketdata/instruments/master',
                                 data=json.dumps({
                                     "exchangeSegmentList": [
                                         "NSECM",
                                         "NSEFO"
                                     ]}),
                                 headers={
                                     'Authorization': "Bearer " + token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'
                                 })
        data = response.json()
        lines = data['result'].splitlines()

        conn = None
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', '127.0.0.1'),
                database=os.environ.get('DB_NAME', 'postgres'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', 'password'),
                port=os.environ.get('DB_PORT', '5432')
            )

            cur = conn.cursor()

            sql = """ INSERT INTO instrument_masters (exchange_segment, exchange_instrument_id, instrument_type, name, 
            description, series, name_with_series, instrument_id, price_band_high, price_band_low, freeze_qty, 
            tick_size, lot_size, underlying_instrument_id, underlying_index_name, contract_expiration, strike_price, 
            option_type) 
            VALUES (%(exchange_segment)s, %(exchange_instrument_id)s, %(instrument_type)s, %(name)s, %(description)s, 
            %(series)s, %(name_with_series)s, %(instrument_id)s, %(price_band_high)s, %(price_band_low)s, 
            %(freeze_qty)s, %(tick_size)s, %(lot_size)s, %(underlying_instrument_id)s, %(underlying_index_name)s, 
            %(contract_expiration)s, %(strike_price)s, %(option_type)s) 
            ON CONFLICT (instrument_id) 
            DO UPDATE SET exchange_segment = %(exchange_segment)s, exchange_instrument_id = %(exchange_instrument_id)s,
            instrument_type = %(instrument_type)s, name = %(name)s, description = %(description)s, series = %(series)s, 
            name_with_series = %(name_with_series)s, price_band_high = %(price_band_high)s, 
            price_band_low = %(price_band_low)s, freeze_qty = %(freeze_qty)s, tick_size = %(tick_size)s, 
            lot_size = %(lot_size)s, underlying_instrument_id = %(underlying_instrument_id)s,
            underlying_index_name = %(underlying_index_name)s, contract_expiration = %(contract_expiration)s, 
            strike_price = %(strike_price)s, option_type = %(option_type)s"""

            for line in lines:
                values = line.split('|')
                for i in range(18 - len(values)):
                    values.append(None)

                cur.execute(sql, {
                    'exchange_segment': values[0],
                    'exchange_instrument_id': values[1],
                    'instrument_type': values[2],
                    'name': values[3],
                    'description': values[4],
                    'series': values[5],
                    'name_with_series': values[6],
                    'instrument_id': values[7],
                    'price_band_high': values[8],
                    'price_band_low': values[9],
                    'freeze_qty': values[10],
                    'tick_size': values[11],
                    'lot_size': values[12],
                    'underlying_instrument_id': values[13],
                    'underlying_index_name': values[14],
                    'contract_expiration': values[15],
                    'strike_price': values[16],
                    'option_type': values[17]
                })

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

import pytest
import requests_mock

from currency_vmms_api import db
from currency_vmms_api.models import PairMMSDailyModel
from scheduler.currencies_mms_scheduler import CurrenciesMMSScheduler
from datetime import datetime, timedelta


class TestCurrenciesMMSScheduler:

    @staticmethod
    @pytest.fixture(autouse=True)
    def create_required_tables_for_analysis():
        db.session.query(PairMMSDailyModel).delete()
        db.session.commit()

    def test_calculate_currency_mms_for_range_100(self):
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=100)
        close_values = [x for x in range(100)]
        expected_keys = ['pair', 'timestamp', 'mms_20', 'mms_50', 'mms_200']
        expected_data = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                         None, None, None, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5,
                         22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5, 33.5, 34.5, 35.5, 36.5, 37.5,
                         38.5, 39.5, 40.5, 41.5, 42.5, 43.5, 44.5, 45.5, 46.5, 47.5, 48.5, 49.5, 50.5, 51.5, 52.5, 53.5,
                         54.5, 55.5, 56.5, 57.5, 58.5, 59.5, 60.5, 61.5, 62.5, 63.5, 64.5, 65.5, 66.5, 67.5, 68.5, 69.5,
                         70.5, 71.5, 72.5, 73.5, 74.5, 75.5, 76.5, 77.5, 78.5, 79.5, 80.5, 81.5, 82.5, 83.5, 84.5, 85.5,
                         86.5, 87.5, 88.5, 89.5]

        pair_mms_rows = CurrenciesMMSScheduler.calculate_currency_mms(close_values, start_date, 'BRLBTC')
        result = [row['mms_20'] for row in pair_mms_rows]
        keys = list(pair_mms_rows[0].keys())

        assert (result, keys) == (expected_data, expected_keys)

    def test_increment_mms_table_with_success(self):
        assert CurrenciesMMSScheduler().increment_mms_table() == (True, None)

    @requests_mock.Mocker(kw="mock")
    def test_increment_mms_table_with_invalid_response_from_candles_api(self, **kwargs):
        kwargs["mock"].get('https://mobile.mercadobitcoin.com.br/v4/BRLBTC/candle', status_code=500)
        expected_message = 'Requisição à API de candles não retornou com sucesso. causa: None, status_code: 500, ' \
                           'Descrição: '

        assert CurrenciesMMSScheduler().increment_mms_table() == (False, expected_message)

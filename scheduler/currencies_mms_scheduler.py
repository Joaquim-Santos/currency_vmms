import requests
import statistics

from currency_vmms_api.services.pair_mms import PairMMSService
from currency_vmms_api.common.exceptions import GenericException, IntegrityException
from scheduler.abstract_scheduler import AbstractScheduler
from datetime import datetime, timedelta
from statistics import StatisticsError


class CurrenciesMMSScheduler(AbstractScheduler):
    def __init__(self):
        super().__init__("currencies_mms_scheduler", 'currencies_mms_scheduler.log', 1440)
        self._service = PairMMSService()
        self._base_url = 'https://mobile.mercadobitcoin.com.br/v4/'
        self._target_currencies = ['BRLBTC', 'BRLETH']
        self._request_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
                                               'Safari/537.36'}

    @staticmethod
    def calculate_currency_mms(close_values: list, start_date: datetime, pair: str):
        close_values.sort(reverse=False)
        pair_mms_rows = []
        target_mms_days = {"mms_20": 20, "mms_50": 50, "mms_200": 200}

        for i in range(len(close_values)):
            row = {
                "pair": pair,
                "timestamp": start_date + timedelta(days=i)
            }
            for key, days in target_mms_days.items():
                try:
                    row[key] = statistics.mean(close_values[i-days+1: i+1])
                except StatisticsError:  # Lista vazia, quando não existem dias suficientes anterior ao atual.
                    row[key] = None

            pair_mms_rows.append(row)

        return pair_mms_rows

    def increment_mms_table(self):
        last_days_by_pair = self._service.get_last_day_of_mms_for_pair()
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=366)
        pair_mms_rows = []

        for pair in self._target_currencies:
            start_date = last_days_by_pair.get(pair, base_date) + timedelta(days=1)
            end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            url_params = {
                'from': int(datetime.timestamp(start_date)),
                'to': int(datetime.timestamp(end_date)),
                'precision': '1d'
            }

            response = requests.get(f"{self._base_url}{pair}/candle", params=url_params,
                                    headers=self._request_headers)
            if response.status_code != 200:
                return False, f"Requisição à API de candles não retornou com sucesso. causa: {response.reason}, " \
                              f"status_code: {response.status_code}, Descrição: {response.text}"

            candles = response.json()["candles"]
            close_values = [item['close'] for item in candles]
            pair_mms_rows.extend(
                CurrenciesMMSScheduler.calculate_currency_mms(close_values, start_date, pair))

        try:
            self._service.get_repository().create_many(pair_mms_rows)
        except (IntegrityException, GenericException) as error:
            return False, error.message

        self._logger_info.log.info(f"Atualização da tabela de MMS com sucesso para os dias: "
                                   f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
        return True, None

    def on_run(self) -> (bool, Exception):
        return self.increment_mms_table()

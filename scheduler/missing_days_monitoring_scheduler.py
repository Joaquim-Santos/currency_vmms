from currency_vmms_api.services.pair_mms import PairMMSService
from scheduler.abstract_scheduler import AbstractScheduler


class MissingDaysMonitoringScheduler(AbstractScheduler):
    def __init__(self):
        super().__init__("missing_days_monitoring_scheduler", 'missing_days_monitoring_scheduler.log', 60)
        self._service = PairMMSService()
        self._target_currencies = ['BRLBTC', 'BRLETH']

    def check_missing_days(self):
        count_days_by_pair = self._service.get_count_days_by_pair()
        has_missing = False

        for pair in self._target_currencies:
            if count_days_by_pair.get(pair, 0) < 365:
                has_missing = True
                break

        if not has_missing:
            self._logger_info.log.info("Não há registros faltantes para os últimos 365 dias.")
        else:
            self._logger_info.log.exception("Há registros faltantes para os últimos 365 dias.")

        return True, None

    def on_run(self) -> (bool, Exception):
        return self.check_missing_days()

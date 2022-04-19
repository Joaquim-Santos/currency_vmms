import threading
from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta
from currency_vmms_api.common.logger import Logger
from currency_vmms_api.configurations.config import get_config


class AbstractScheduler(ABC):

    def __init__(self, log_name: str, log_file_name: str, frequency_in_minutes: int):
        self._frequency_in_minutes = frequency_in_minutes
        self._retries = 5
        self._current_retry = 0
        self._logger_info = Logger(get_config(), log_name, log_file_name)

    @property
    def frequency_in_minutes(self):
        return self._frequency_in_minutes

    @frequency_in_minutes.setter
    def frequency_in_minutes(self, frequency_in_minutes):
        self._frequency_in_minutes = frequency_in_minutes

    @property
    def retries(self):
        return self._retries

    @retries.setter
    def retries(self, retries):
        self._retries = retries

    @abstractmethod
    def on_run(self) -> (bool, Exception):
        raise Exception("Method must be implemented")

    def _schedule(self, time_in_minutes):
        now = datetime.now()
        run_at = now + timedelta(minutes=time_in_minutes)
        delay = (run_at - now).total_seconds()
        threading.Timer(delay, self.run).start()

    def schedule(self, run_now: bool = False):
        if run_now:
            self._schedule(0)
        self._schedule(self.frequency_in_minutes)

    def try_again(self):
        self._logger_info.log.exception(
            f"Scheduler {type(self).__name__} falhou, tentar novamente em {self._current_retry} minuto(s).")
        self._schedule(self._current_retry)

    def run(self):
        success, exception = self.on_run()
        if success:
            self.schedule()
        elif self._current_retry < self._retries:
            self._current_retry += 1
            self._logger_info.log.exception(exception)
            self.try_again()
        else:
            self._current_retry = 0
            self.schedule()

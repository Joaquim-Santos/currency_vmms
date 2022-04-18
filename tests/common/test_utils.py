from datetime import datetime, timedelta

from currency_vmms_api.common.utils import Utils


class TestUtils:

    def test_get_timestamp_number_from_some_day_before_now(self):
        target_day = (datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        assert datetime.timestamp(target_day) == \
               Utils.get_timestamp_number_from_some_day_before_now(1)

    def test_convert_timestamp_number_to_datetime(self):
        assert datetime(2022, 4, 16, 0, 0, 0) == Utils.convert_timestamp_number_to_datetime(1650153600)

    def test_get_datetime_from_some_day_before_now(self):
        assert (datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) == \
               Utils.get_datetime_from_some_day_before_now(1)

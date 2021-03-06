from currency_vmms_api.services.pair_mms import PairMMSService
from currency_vmms_api.common.utils import Utils


class TestPairMMSService:

    def test_get_mms_variations_by_time_course_with_data(self):
        data = {
            "pair": "BRLETH",
            "start_date": Utils.get_datetime_from_some_day_before_now(2),
            "end_date": Utils.get_datetime_from_some_day_before_now(2),
            "range": 200
        }
        expected_data = [
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(2), 'mms': 12.0}
        ]

        assert PairMMSService().get_mms_variations_by_time_course(data) == expected_data

    def test_get_mms_variations_by_time_course_without_data(self):
        data = {
            "pair": "BRLETH",
            "start_date": Utils.get_datetime_from_some_day_before_now(4),
            "end_date": Utils.get_datetime_from_some_day_before_now(3),
            "range": 200
        }

        assert PairMMSService().get_mms_variations_by_time_course(data) == []

    def test_get_last_day_of_mms_for_pair_with_success(self):
        expected_data = {
            'BRLBTC': Utils.get_datetime_from_some_day_before_now(0),
            'BRLETH': Utils.get_datetime_from_some_day_before_now(0)
        }

        assert PairMMSService().get_last_day_of_mms_for_pair() == expected_data

    def test_get_count_days_by_pair_with_success(self):
        expected_data = {
            'BRLBTC': 3,
            'BRLETH': 3
        }

        assert PairMMSService().get_count_days_by_pair() == expected_data

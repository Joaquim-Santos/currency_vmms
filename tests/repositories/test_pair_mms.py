from currency_vmms_api.repositories.pair_mms import PairMMSRepository
from currency_vmms_api.common.utils import Utils


class TestPairMMSRepository:

    def test_get_mms_variations_by_time_course_with_success(self):
        data = {
            "pair": "BRLBTC",
            "start_date": Utils.get_datetime_from_some_day_before_now(2),
            "end_date": Utils.get_datetime_from_some_day_before_now(1),
            "range": 50
        }
        expected_data = [
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(2), 'mms': 21.0},
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(1), 'mms': 21.1}
        ]

        assert PairMMSRepository().get_mms_variations_by_time_course(data) == expected_data

    def test_get_last_day_of_mms_for_pair_with_success(self):
        expected_data = {
            'BRLBTC': Utils.get_datetime_from_some_day_before_now(0),
            'BRLETH': Utils.get_datetime_from_some_day_before_now(0)
        }

        assert PairMMSRepository().get_last_day_of_mms_for_pair() == expected_data

    def test_get_count_days_by_pair_with_success(self):
        expected_data = {
            'BRLBTC': 3,
            'BRLETH': 3
        }

        assert PairMMSRepository().get_count_days_by_pair() == expected_data

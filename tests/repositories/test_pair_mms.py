from currency_vmms_api.repositories.pair_mms import PairMMSRepository
from currency_vmms_api.common.utils import Utils


class TestPairMMSRepository:

    def test_get_mms_variations_by_time_course_with_success(self, client):
        data = {
            "pair": "BRLBTC",
            "start_date": Utils.get_datetime_from_some_day_before_now(2),
            "end_date": Utils.get_datetime_from_some_day_before_now(1),
            "range": 50
        }
        expected_data = [
            {'timestamp': 1649991600.0, 'mms': 21.0},
            {'timestamp': 1650078000.0, 'mms': 21.1}
        ]

        assert PairMMSRepository().get_mms_variations_by_time_course(data) == expected_data

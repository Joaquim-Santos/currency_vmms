import json

from http import HTTPStatus

from currency_vmms_api.common.utils import Utils


class TestPairMMSResource:

    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/BRLBTC/mms")
        responses_status.append(response.status_code)

        response = client.put("/api/BRLBTC/mms")
        responses_status.append(response.status_code)

        response = client.delete("/api/BRLBTC/mms")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.INTERNAL_SERVER_ERROR
        ]

    def test_get_with_success(self, client):
        expected_data = [
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(2), 'mms': 20.0},
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(1), 'mms': 20.1},
            {'timestamp': Utils.get_timestamp_number_from_some_day_before_now(0), 'mms': 20.2}
        ]
        data = {
            "from": Utils.get_timestamp_number_from_some_day_before_now(2),
            "to": Utils.get_timestamp_number_from_some_day_before_now(0),
            "range": 20
        }

        response = client.get("/api/BRLBTC/mms", query_string=data)

        assert (json.loads(response.data, encoding='utf-8'), response.status_code) == \
               (expected_data, HTTPStatus.OK)

    def test_get_with_bad_request(self, client):
        expected_message = {
            'error_message': {'range': ['Must be one of: 20, 50, 200.']}
        }
        data = {
            "from": Utils.get_timestamp_number_from_some_day_before_now(2),
            "to": Utils.get_timestamp_number_from_some_day_before_now(0),
            "range": 201
        }

        response = client.get("/api/BRLBTC/mms", query_string=data)

        assert (json.loads(response.data, encoding='utf-8'), response.status_code) == (expected_message,
                                                                                       HTTPStatus.BAD_REQUEST)

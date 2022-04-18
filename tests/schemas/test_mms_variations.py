import pytest

from currency_vmms_api.schemas.mms_variations import MMSVariationsInputSchema
from currency_vmms_api.common.utils import Utils
from marshmallow.exceptions import ValidationError


class TestMMSVariationsInputSchema:
    @pytest.fixture(autouse=True)
    def init_stuff(self):
        self.schema = MMSVariationsInputSchema()
        self.data = {
          "pair": "BRLETH",
          "start_date": Utils.get_timestamp_number_from_some_day_before_now(365),
          "end_date": Utils.get_timestamp_number_from_some_day_before_now(0),
          "range": 20
        }

    def test_mms_variations_input_schema_with_valid_data(self):
        result = self.schema.validate(self.data)
        assert result == {}

    def test_mms_variations_input_schema_with_valid_data_with_default_end_date(self):
        del self.data['end_date']
        result = self.schema.load(self.data)
        end_date = Utils.get_timestamp_number_from_some_day_before_now(1)
        end_date = Utils.convert_timestamp_number_to_datetime(end_date)

        assert result['end_date'] == end_date

    def test_mms_variations_input_schema_with_missing_required_field(self):
        self.data = {}

        result = self.schema.validate(self.data)

        assert result == {
            "pair": [
                "Missing data for required field."
            ],
            "start_date": [
                "Missing data for required field."
            ],
            "range": [
                "Missing data for required field."
            ]
        }

    def test_mms_variations_input_schema_with_missing_invalid_pair(self):
        expected_errors = []
        self.data['pair'] = 1

        result = self.schema.validate(self.data)
        expected_errors.append(result)

        self.data['pair'] = 'BRLET'

        result = self.schema.validate(self.data)
        expected_errors.append(result)

        assert expected_errors == [
            {
                'pair': ['Not a valid string.']
            },
            {
                'pair': ['Must be one of: BRLBTC, BRLETH.']
            }
        ]

    def test_mms_variations_input_schema_with_missing_invalid_range(self):
        expected_errors = []
        self.data['range'] = 'a'

        result = self.schema.validate(self.data)
        expected_errors.append(result)

        self.data['range'] = 21

        result = self.schema.validate(self.data)
        expected_errors.append(result)

        assert expected_errors == [
            {
                'range': ['Not a valid integer.']
            },
            {
                'range': ['Must be one of: 20, 50, 200.']
             }
        ]

    def test_mms_variations_input_schema_with_missing_invalid_start_date_and_end_date(self):
        self.data['start_date'] = 'a'
        self.data['end_date'] = 'b'

        result = self.schema.validate(self.data)

        assert result == {
            'start_date': ['Not a valid integer.'],
            'end_date': ['Not a valid integer.']
        }

    def test_mms_variations_input_schema_with_missing_start_date_bigger_than_end_date(self):
        self.data['start_date'] = Utils.get_timestamp_number_from_some_day_before_now(364)
        self.data['end_date'] = Utils.get_timestamp_number_from_some_day_before_now(365)

        try:
            self.schema.load(self.data)
            raise AssertionError
        except ValidationError as error:
            assert error.messages == {
                '_schema': ["Data inicial não pode ser maior do que a final."]
            }

    def test_mms_variations_input_schema_with_missing_start_date_before_365_days_agos(self):
        self.data['start_date'] = Utils.get_timestamp_number_from_some_day_before_now(366)

        try:
            self.schema.load(self.data)
            raise AssertionError
        except ValidationError as error:
            assert error.messages == {
                '_schema': ["Não permitidas consultas cuja data de início seja anterior a 365 dias."]
            }

    def test_mms_variations_input_schema_with_missing_end_date_after_now(self):
        self.data['end_date'] = Utils.get_timestamp_number_from_some_day_before_now(-1)

        try:
            self.schema.load(self.data)
            raise AssertionError
        except ValidationError as error:
            assert error.messages == {
                '_schema': ["Não permitidas consultas cuja data final seja maior do que a atual."]
            }

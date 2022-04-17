from currency_vmms_api.common.utils import Utils

from marshmallow import Schema, fields, EXCLUDE, validate, post_load
from marshmallow.exceptions import ValidationError


class MMSVariationsInputSchema(Schema):
    pair = fields.Str(required=True, validate=[validate.OneOf(['BRLBTC', 'BRLETH'])])
    start_date = fields.Int(required=True)
    end_date = fields.Int(frequired=False, allow_none=True)
    range = fields.Int(required=True, validate=[validate.OneOf([20, 50, 200])])

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, many, **kwargs):
        # Se a data final não é informada, usa-se o default do dia anterior.
        if not data.get('end_date'):
            data['end_date'] = Utils.get_timestamp_number_from_some_day_before_now(1)

        if data.get('start_date') > data.get('end_date'):
            raise ValidationError("Data inicial não pode ser maior do que a final.")

        if data.get('start_date') < Utils.get_timestamp_number_from_some_day_before_now(365):
            raise ValidationError("Não permitidas consultas cuja data de início seja anterior a 365 dias.")

        if data.get('end_date') > Utils.get_timestamp_number_from_some_day_before_now(0):
            raise ValidationError("Não permitidas consultas cuja data final seja maior do que a atual.")

        data['start_date'] = Utils.convert_timestamp_number_to_datetime(data['start_date'])
        data['end_date'] = Utils.convert_timestamp_number_to_datetime(data['end_date'])

        return data

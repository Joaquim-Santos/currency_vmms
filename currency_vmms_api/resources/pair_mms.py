from currency_vmms_api.common.abstract_resource import AbstractResource
from currency_vmms_api.schemas import MMSVariationsInputSchema
from currency_vmms_api.common.exceptions import BadRequest

from flasgger import swag_from
from flask import request
from marshmallow.exceptions import ValidationError


class PairMMSResource(AbstractResource):
    service_module = 'currency_vmms_api.services.pair_mms'
    service_class = 'PairMMSService'

    @swag_from("../swagger/models/pair_mms/pair-mms-get.yml", endpoint="api.pair_mms")
    def get(self, **kwargs):
        pair_mms_filters = {
            'pair': request.view_args['pair'],
            'start_date': request.args.get('from'),
            'end_date': request.args.get('to'),
            'range': request.args.get('range')
        }

        schema = MMSVariationsInputSchema()
        try:
            pair_mms_filters = schema.load(pair_mms_filters)
        except ValidationError as error:
            raise BadRequest(message=error.messages)

        return self.get_service().get_mms_variations_by_time_course(pair_mms_filters)

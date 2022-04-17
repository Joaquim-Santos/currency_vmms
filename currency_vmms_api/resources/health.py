from currency_vmms_api.common.abstract_resource import AbstractResource
from datetime import datetime
from flasgger import swag_from


class HealthResource(AbstractResource):
    service_module = ''
    service_class = ''

    @swag_from("../swagger/models/health/health.yml", endpoint="api.health")
    def get(self, **kwargs):
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S')

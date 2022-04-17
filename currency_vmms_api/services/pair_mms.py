from currency_vmms_api.common.abstract_service import AbstractService


class PairMMSService(AbstractService):
    repository_module = 'currency_vmms_api.repositories.pair_mms'
    repository_class = 'PairMMSRepository'

    def get_mms_variations_by_time_course(self, pair_mms_filters: dict):
        return self.get_repository().get_mms_variations_by_time_course(pair_mms_filters)

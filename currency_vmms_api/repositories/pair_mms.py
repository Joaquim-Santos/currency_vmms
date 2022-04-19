from currency_vmms_api.common.abstract_repository import AbstractRepository
from currency_vmms_api.models import PairMMSDailyModel
from currency_vmms_api import db
from datetime import datetime
from sqlalchemy import func


class PairMMSRepository(AbstractRepository):
    model_module = 'currency_vmms_api.models.pair_mms_daily'
    model_class = 'PairMMSDailyModel'

    def get_mms_variations_by_time_course(self, pair_mms_filters: dict):
        query_result = PairMMSDailyModel.query \
            .filter((PairMMSDailyModel.pair == pair_mms_filters['pair']) &
                    (PairMMSDailyModel.timestamp >= pair_mms_filters['start_date']) &
                    (PairMMSDailyModel.timestamp <= pair_mms_filters['end_date'])) \
            .order_by(PairMMSDailyModel.timestamp) \
            .all()

        result = []
        possible_mms = {
            20: "mms_20",
            50: "mms_50",
            200: "mms_200"
        }

        for item in query_result:
            item = item.to_dict()
            selected_mms = possible_mms[pair_mms_filters['range']]

            selected_item = {
                "timestamp": int(datetime.timestamp(item["timestamp"])),
                "mms": item[selected_mms]
            }

            result.append(selected_item)

        return result

    def get_last_day_of_mms_for_pair(self):
        query_result = db.session.query(PairMMSDailyModel.pair,
                                        func.max(PairMMSDailyModel.timestamp).label('last_day'))\
            .group_by(PairMMSDailyModel.pair)\
            .all()

        result = {}
        for item in query_result:
            item = dict(item)
            result[item['pair']] = item['last_day']

        return result

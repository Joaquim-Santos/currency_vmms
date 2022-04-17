from currency_vmms_api import db
from currency_vmms_api.common.abstract_model import AbstractModel


class PairMMSDailyModel(db.Model, AbstractModel):
    __tablename__ = 'pair_mms_daily'

    pair = db.Column(db.String(6), nullable=False, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, primary_key=True)
    mms_20 = db.Column(db.Float, nullable=True)
    mms_50 = db.Column(db.Float, nullable=True)
    mms_200 = db.Column(db.Float, nullable=True)

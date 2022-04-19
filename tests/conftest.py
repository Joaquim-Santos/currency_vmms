import pytest
import os

from currency_vmms_api import application, db
from currency_vmms_api.models import *
from currency_vmms_api.common.utils import Utils

from shutil import rmtree


@pytest.fixture(scope="session")
def app():
    with application.app_context():
        yield application


@pytest.fixture(scope="session", autouse=True)
def create_db():
    rmtree('tests/databases', ignore_errors=True)
    os.mkdir('tests/databases')

    db.create_all()
    db.session.commit()


@pytest.fixture(scope="module", autouse=True)
def create_required_tables_for_analysis():
    db.session.query(PairMMSDailyModel).delete()

    pair_mms_daily_data = []

    # Criar dados de MMS para cada moeda.
    pair_mms_daily_1 = {
      "pair": "BRLETH",
      "timestamp": Utils.get_datetime_from_some_day_before_now(2),
      "mms_20": 10.0,
      "mms_50": 11.0,
      "mms_200": 12.0
    }

    pair_mms_daily_2 = {
      "pair": "BRLETH",
      "timestamp": Utils.get_datetime_from_some_day_before_now(1),
      "mms_20": 10.1,
      "mms_50": 11.1,
      "mms_200": 12.1
    }

    pair_mms_daily_3 = {
      "pair": "BRLETH",
      "timestamp": Utils.get_datetime_from_some_day_before_now(0),
      "mms_20": 10.2,
      "mms_50": 11.2,
      "mms_200": 12.2
    }

    pair_mms_daily_4 = {
        "pair": "BRLBTC",
        "timestamp": Utils.get_datetime_from_some_day_before_now(2),
        "mms_20": 20.0,
        "mms_50": 21.0,
        "mms_200": 22.0
    }

    pair_mms_daily_5 = {
        "pair": "BRLBTC",
        "timestamp": Utils.get_datetime_from_some_day_before_now(1),
        "mms_20": 20.1,
        "mms_50": 21.1,
        "mms_200": 22.1
    }

    pair_mms_daily_6 = {
        "pair": "BRLBTC",
        "timestamp": Utils.get_datetime_from_some_day_before_now(0),
        "mms_20": 20.2,
        "mms_50": 21.2,
        "mms_200": 22.2
    }
    pair_mms_daily_data.extend([pair_mms_daily_1, pair_mms_daily_2, pair_mms_daily_3,
                                pair_mms_daily_4, pair_mms_daily_5, pair_mms_daily_6])

    for pair_mms_row in pair_mms_daily_data:
        pair_mms_daily_model = PairMMSDailyModel(**pair_mms_row)
        db.session.add(pair_mms_daily_model)

    db.session.commit()

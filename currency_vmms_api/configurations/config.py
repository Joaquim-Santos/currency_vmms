import importlib
import os


class BaseConfig:

    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    LOCAL_VALIDATION = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DB_SCHEMA = os.environ.get("DB_SCHEMA")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", 3307)
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}'

    MAIL_USER = os.environ.get("MAIL_USER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    NOTIFICATION_EMAIL = os.environ.get("NOTIFICATION_EMAIL")

    LOGS_FOLDER = os.environ.get("LOGS_FOLDER")

    SWAGGER = {
        'title': "Currency VMMS",
        'version': 1,
        'description': "Currency VMMS Endpoints"
    }


class TestConfig(BaseConfig):
    DEBUG = True
    LOCAL_VALIDATION = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/databases/currency_vmms_test.db'


class LocalConfig(BaseConfig):
    DEBUG = True
    LOCAL_VALIDATION = True

    SQLALCHEMY_ECHO = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config():
    return getattr(importlib.import_module('currency_vmms_api.configurations.config'),
                   os.environ['STAGE'].capitalize() + 'Config')

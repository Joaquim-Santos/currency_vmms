# -*- coding: utf-8 -*-
import importlib
import json

from flask import Blueprint, Flask
from flask_restful import Api as FlaskApi
from flask_cors import CORS


class RoutesBuilder:

    @staticmethod
    def mount_flask_uri(method):
        method_uri = method['path']
        if method.get("queryParams", []):
            for param in method['queryParams']:
                method_uri = method_uri + '/<' + param['type'] + ':' + param['name'] + '>'
        return method_uri

    @staticmethod
    def add_resources(application: Flask, router_file_path: str) -> None:
        """
           Função que registra as rotas da aplicação, que foram definidas em JSON.

           Parameters
           ----------
           application: Flask
               Aplicação configurada para ter as rotas inseridas.

            router_file_path: str
               Arquivo JSON com a definição das rotas, em formato determinado, que inclui métodos, cabeçalhos e
               módulos correspondentes às rotas.

       """
        with open(router_file_path, 'r') as routes_file:
            data = json.load(routes_file)

        api_bp = Blueprint(data['blueprint']['name'], application.import_name)
        api = FlaskApi(api_bp)

        for resource in data['blueprint']['resources']:
            urls = []
            # Construct URLs
            for method in resource['methods']:
                urls.append(method['path'])

            # Criar recurso para URLs
            api.add_resource(
                getattr(importlib.import_module(
                    resource['flask']['resourceModule']),
                    resource['flask']['resourceClass']
                ),
                *urls,
                endpoint=resource['name'],
                strict_slashes=resource['flask']['strictSlashes']
            )

        application.register_blueprint(api_bp, url_prefix=data['blueprint']['url_prefix'])

    @staticmethod
    def add_cors(application: Flask, router_file_path: str) -> None:
        """
           Função que ativa CORS para rotas, segundo configuração definida em JSON.

           Parameters
           ----------
           application: Flask
               Aplicação configurada para ter CORS ativado.

            router_file_path: str
               Arquivo JSON com a definição das rotas, em formato determinado, que inclui métodos, cabeçalhos e
               módulos correspondentes às rotas.

       """

        with open(router_file_path, 'r') as routes_file:
            data = json.load(routes_file)

        blueprint = data['blueprint']

        url_prefix = blueprint['url_prefix']
        resources_config = {}
        for resource in blueprint['resources']:
            for method in resource['methods']:
                if not method["cors"]["enable"]:
                    continue
                url = rf'{url_prefix}{method["path"]}*'
                resources_config[url] = {
                    "origins": method["cors"]["origins"],
                    "methods": method["cors"]["methods"],
                    "allow_headers": method["cors"]["allowHeaders"]
                }

        CORS(application, resources=resources_config)

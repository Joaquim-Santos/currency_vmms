import importlib

from flask import request
from flask_restful import Resource

from currency_vmms_api.common.exceptions import MethodNotAllowed, EntityNotFound


class AbstractResource(Resource):
    """
        Classe abstrata para criar recursos.
    """
    @property
    def service_module(self):
        """
            String para o caminho do módulo do serviço.
        """
        raise NotImplementedError

    @property
    def service_class(self):
        """
            String para o nome da classe do serviço.
        """
        raise NotImplementedError

    def get_service(self):
        """
            Método para retornar uma instância do módulo de serviço.

            Returns
            ----------
            Object
                Uma instância do serviço especificado no atributo 'service_class'.
        """
        service_class = getattr(importlib.import_module(self.service_module), self.service_class)
        return service_class()

    def get(self):
        """
            Método para lidar com requisição HTTP GET.
        """
        raise MethodNotAllowed

    def post(self):
        """
            Método para lidar com requisição HTTP POST.
        """
        raise MethodNotAllowed

    def put(self):
        """
            Método para lidar com requisição HTTP PUT.
        """
        raise MethodNotAllowed

    def delete(self):
        """
            Método para lidar com requisição HTTP DELETE.
        """
        raise MethodNotAllowed

    def get_headers_request(self):
        """
            Returns
            ----------
            dict
               Cabeçalho da requisição como um dicionário.

       """
        return request.headers

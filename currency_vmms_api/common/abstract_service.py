import importlib
from abc import ABC, abstractmethod


class AbstractService(ABC):
    """
        Classe abstrata para criar serviços.
    """

    @property
    @abstractmethod
    def repository_module(self):
        """
            String para o caminho do módulo do repositório.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def repository_class(self):
        """
            String para o nome da classe do repositório.
        """
        raise NotImplementedError

    def get_repository(self):
        """
            Método para retornar uma instância do módulo de repositório.

            Returns
            ----------
            Object
                Uma instância do repositório especificado no atributo 'repository_class'.
        """
        service_class = getattr(importlib.import_module(self.repository_module), self.repository_class)
        return service_class()

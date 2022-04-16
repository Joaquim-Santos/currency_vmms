from abc import abstractmethod

from sqlalchemy.orm.state import InstanceState

from currency_vmms_api.common.serializer import Serializer


class AbstractModel:
    """
        Classe abstrata para criar modelos.
    """

    @property
    @abstractmethod
    def __tablename__(self):
        """
            String do nome da tabela que o modelo irá mapear.
        """
        raise NotImplementedError

    def to_json(self):
        """
            Método que cria um JSON das colunas do modelo com seus valores serializados.

            Returns
            ----------
            dict
                Contém o mapeamento das colunas do modelo e seus valores.
        """
        json = {}
        for key in self.to_dict():
            if type(getattr(self, key)) is not InstanceState:
                json[key] = Serializer.json_serialize(getattr(self, key))
        return json

    def to_dict(self):
        """
            Método que cria um dicionário das colunas do modelo e seus valores.

            Returns
            ----------
            dict
                Contém o mapeamento das colunas do modelo e seus valores.
        """
        return dict((column.name, getattr(self, column.name)) for column in self.__table__.columns)

    def __repr__(self):
        """
            Método que cria uma representação do modelo com seus atributos.

            Returns
            ----------
            String
        """
        return "%s(%r)" % (self.__class__, self.__dict__)

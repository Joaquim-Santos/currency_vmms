from datetime import datetime, date
import json
from decimal import Decimal

from sqlalchemy.orm.state import InstanceState

from currency_vmms_api.common.exceptions.type_not_identified import TypeNotIdentified


class Serializer:
    """
        Classe responsável por fornecer serialização para mostrar qualquer objeto.
    """

    @staticmethod
    def json_serialize(element):
        """
            Método para serializar qualquer elemento pelo seu tipo para ser colocado em objeto JSON.

            Parameters
            ----------
            element: any
                Elemento para ser serializado.

            Raises
            ----------
            TypeNotIdentified
                Se o tipo do elemento não pode ser identificado durante a serialização.
        """
        if type(element) is str or type(element) is int or type(element) is float or type(element) is bool or \
           type(element) is list or element is None:
            return element
        if type(element) is dict:
            return json.dumps(element, indent=4, sort_keys=True, default=str)
        elif type(element) is Decimal:
            return float(element)
        elif type(element) is date:
            return element.strftime('%Y-%m-%d')
        elif type(element) is datetime:
            return datetime.isoformat(element)
        elif type(element) is InstanceState or type(element) is bytes:
            return None
        else:
            raise TypeNotIdentified(f'Cannot identify type: {type(element)}')

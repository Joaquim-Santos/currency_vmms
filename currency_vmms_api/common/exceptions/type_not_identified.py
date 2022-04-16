from currency_vmms_api.common.abstract_exception import AbstractException


class TypeNotIdentified(AbstractException):

    def __init__(self, message='Tipo não identificado.', status_code=500, payload=None):
        """
            Exceção lançada quando o tipo de um objeto não é identificado.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 500

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

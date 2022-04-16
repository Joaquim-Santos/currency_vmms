from currency_vmms_api.common.abstract_exception import AbstractException


class CustomerNotIdentified(AbstractException):
    def __init__(self, message='Não foi possível identificar o cliente ou permissão negada.', status_code=401, payload=None):
        """
            Exceção para quando o cliente não pode ser identificado ou teve acesso negado.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 401

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

from currency_vmms_api.common.abstract_exception import AbstractException


class IntegrityException(AbstractException):
    def __init__(self, message='Erro de integridade.', status_code=409, payload=None):
        """
            Exceção para quando ocorre falha de integridade no banco de dados.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 409

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

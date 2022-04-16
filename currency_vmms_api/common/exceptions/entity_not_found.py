from currency_vmms_api.common.abstract_exception import AbstractException


class EntityNotFound(AbstractException):

    def __init__(self, message='Entidade não encontrada.', status_code=404, payload=None):
        """
            Exceção para quando uma entidade não pode ser encontrada.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 404

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

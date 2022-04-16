from currency_vmms_api.common.abstract_exception import AbstractException


class MethodNotAllowed(AbstractException):

    def __init__(self, message='Método não permitido.', status_code=405, payload=None):
        """
            O método solicitado ao servidor não pode ser usado.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 405

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

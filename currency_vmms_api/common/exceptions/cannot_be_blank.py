from currency_vmms_api.common.abstract_exception import AbstractException


class CannotBeBlank(AbstractException):

    def __init__(self, message='Campo não pode ser branco.', status_code=400, payload=None):
        """
            Exceção para quando o campo não pode estar em branco.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 400

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

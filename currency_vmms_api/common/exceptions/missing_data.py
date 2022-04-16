from currency_vmms_api.common.abstract_exception import AbstractException


class MissingData(AbstractException):

    def __init__(self, message='Dados não foram informados corretamente.', status_code=422, payload=None):
        """
            A requisição está bem formada mas inabilitada para ser seguida devido a erros semânticos.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 422

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)

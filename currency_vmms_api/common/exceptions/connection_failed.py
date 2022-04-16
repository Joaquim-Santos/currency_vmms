from currency_vmms_api.common.abstract_exception import AbstractException


class ConnectionFailed(AbstractException):

    def __init__(self, message='Não foi possível conectar-se com o serviço requisitado.', status_code=500, payload=None):
        """
            Exceção para quando uma conexão falha, podendo ser usada para qualquer tipo de conexão,
            como de banco de dados ou outro serviço.

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

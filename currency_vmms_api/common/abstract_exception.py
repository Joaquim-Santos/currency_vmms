

class AbstractException(Exception):
    """
        Classe abstrata para criar exceções.

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
    def __init__(self, message='Exceção abstrata.', status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
            Método para criar um dicionário a partir do objedo da exceção.

            Returns
            ----------
            dict
                { 'error_message': self.message } + self.payload
        """
        return_value = dict(self.payload or ())
        return_value['error_message'] = self.message
        return return_value

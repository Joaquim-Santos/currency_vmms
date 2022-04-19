import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:

    mail_host = "smtp.gmail.com"
    mail_port = 587
    user = os.environ.get('MAIL_USER')
    password = os.environ.get('MAIL_PASSWORD')
    recipient_mail = os.environ.get('NOTIFICATION_EMAIL')

    def send_mail(self):
        smtp = None
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.recipient_mail
            msg['Subject'] = "Notificação - Currency VMMS API"

            text = MIMEText(Email.standard_email_body(), 'html', 'utf-8')
            msg.attach(text)

            smtp = smtplib.SMTP(self.mail_host, self.mail_port)
            smtp.ehlo()
            smtp.starttls()

            smtp.login(self.user, self.password)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
            smtp.quit()
        except Exception as exception:
            raise exception
        finally:
            if smtp:
                smtp.close()

    @staticmethod
    def standard_email_body():
        return f"""
                <html>
    <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css?family=Cabin" rel="stylesheet">
    </head>

    <body>
        <div align="center" style="padding-bottom:20px; max-width: 1000px; margin: auto;">
            <h1 style="width:450px;font-family: 'cabin';font-weight: bold;font-size:1.5em;color: #0055ff;text-align: center;padding-bottom:15px">Currency VMMS API - Notificações de Falhas</h1>
            <p style="width:650px;font-family: 'cabin';font-size:20px;color: #4c4c4c;text-align: justify;line-height:30px;padding-bottom:15px">
                Esse e-mail indica que foram encontrados <span style="font-weight: bold">Registros faltantes na base de dados da API</span>, 
                referentes aos dados de MMS das moedas para os últimos 365 dias. Favor verificar a situação. 
            </p>
            <p style="width:650px;font-family: 'cabin';font-size:20px;color: #4c4c4c;text-align: center;line-height:30px;padding-bottom:15px">
                Caso já tenha tratado a falha, favor desconsiderar este email. <br/>
                Esta é uma mensagem automática. Favor não responder.    
            </p>        
        </div>
    </body>
</html>
        """

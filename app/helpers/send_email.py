import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(".env")

logging.basicConfig(level=logging.INFO)


class SettingsEmail(BaseSettings):
    """Configurações de email para envio de confirmação de cadastro"""
    email_remetente: str
    password_remetente: str
    email_destinatario: str

    class Config:
        case_sensitive = True


class SendConfirmationEmail(SettingsEmail):
    """
    Classe para envio de email de confirmação de cadastro.

    A senha do email é gerada no link: https://security.google.com/settings/security/apppasswords
    """

    def send_email(self, email: str, title_email: str, body: str) -> str:

        try:
            # Instanciando o objeto MIMEMultipart
            msg = MIMEMultipart()
            msg['From'] = self.email_remetente
            msg['To'] = email

            # Título do e-mail
            msg['Subject'] = title_email

            msg.attach(MIMEText(body, 'plain'))

            # Servidor de envio de email
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.ehlo()

            # Segurança
            server.starttls()
            server.ehlo()
            server.login(self.email_remetente, self.password_remetente)

            # Envia e email e converte para string e fecha a conexão
            server.sendmail(self.email_remetente, email, msg.as_string())
            logging.info(f"Email enviado com sucesso para: {email}")
            server.quit()

        except Exception as e:
            return str(f"Erro ao enviar o email: {e}")

import smtplib
from datetime import datetime as dt

from config import Config


class SMTPSender:

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.server = smtplib.SMTP_SSL(self.config.smtp_host, 465)
        self.server.login(self.config.smtp_user, self.config.smtp_password)

    def send_mail(self, to: str, subject: str, content: str) -> Exception | None:
        try:
            msg = f"Subject: {subject}\n\n{content}"
            self.server.sendmail(self.config.smtp_user, to, msg)
        except Exception as e:
            return e

    def test_send(self) -> Exception | None:
        self.send_mail(self.config.test_address, "test email", "test content")


def main():
    sender = SMTPSender()
    sender.test_send()


if __name__ == "__main__":
    main()

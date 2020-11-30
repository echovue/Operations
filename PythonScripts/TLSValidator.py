from urllib.request import ssl, socket
import datetime, smtplib

hostname = "etsy.com"
port = '443'

context = ssl.create_default_context()

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        certificate = ssock.getpeercert()

certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')

daysToExpiration = (certExpires - datetime.datetime.now()).days


def send_notification(days_to_expire):
    smtp_port = 587
    smtp_server = "smtp.acmecorp.com"
    sender_email = "operations@acmecorp.com"
    receiver_email = "webmaster@acmecorp.com"
    password = input("Type your password and press enter: ")
    if days_to_expire == 1:
        days = "1 day"
    else:
        days = str(days_to_expire) + " days"

    message = """\
        Subject: Certificate Expiration

        The TLS Certificate for your site expires in {days}"""

    email_context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=email_context)
        server.login(sender_email, password)
        server.sendmail(sender_email,
                        receiver_email,
                        message.format(days=days))


if daysToExpiration == 7 or daysToExpiration == 1:
    send_notification(daysToExpiration)

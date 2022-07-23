from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from FaceDetection import settings
FROM_EMAIL = settings.EMAIL_HOST_USER


def registration_mail(name, no, username, password, to):
    subject, from_email, to_emails = 'Bank Registration Done Successfully', FROM_EMAIL, [to]
    html_content = render_to_string('../templates/emails/register_success.html', {'name': name, 'accno':no, 'loginid':username, 'loginpass':password})
    msg = EmailMessage(subject=subject, body=html_content, from_email=from_email, to=to_emails)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()

def transaction_table(uqs,debit, deposit):
    html_content = render_to_string('../templates/emails/transaction.html',{'uqs': uqs, 'debit': debit, 'deposit': deposit})
    return html_content
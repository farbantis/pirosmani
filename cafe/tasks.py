from django.core.mail import send_mail
from account.models import CustomerAdd
from pirosmani.celery import app
from pirosmani.utils.constants import EMAIL_NEW_USER_REG
from celery import shared_task


# @shared_task
@app.task
def transaction_email_notification(user):
    email = user.email
    subject = f'registration confirmation'
    message = f"""
        Dear {email},
        you successfully placed the order
        the receipt is attached to this letter.
        your status is {user.customeradd.status}.
    """
    from_email = EMAIL_NEW_USER_REG
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

from django.core.mail import send_mail
from pirosmani.utils.constants import EMAIL_NEW_USER_REG


def transaction_email_notification(user):
    email = user.user.email
    subject = f'registration confirmation'
    message = f"""
        Dear {email},
        you successfully placed the order
        the receipt is attached to this letter.
        your status is {user.status}.
    """
    from_email = EMAIL_NEW_USER_REG
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

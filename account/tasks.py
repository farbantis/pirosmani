from celery import shared_task
from django.core.mail import send_mail
from pirosmani.utils.constants import EMAIL_NEW_USER_REG


@shared_task(expires=3600)  # time to execute - 1 hour
def new_user_email_notification(user):
    email = user.user.email
    subject = f'registration confirmation'
    message = f"""
        Dear {email},
        you successfully registered with pirosmani
        your status is {user.status}
    """
    from_email = EMAIL_NEW_USER_REG
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@shared_task
def change_status_notification(user, status, action_status):
    subject = f"cinema - status update notification"
    message = f"""Dear {user},
     {'we are pleased ' if action_status == 'going_up' 
                        else 'it is with regret that we have'}
     to inform you that your status has been updated. 
     It is now {status}"""
    from_email = EMAIL_NEW_USER_REG
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list,)

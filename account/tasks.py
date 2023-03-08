from celery import shared_task
from django.core.mail import send_mail


@shared_task
def change_status_notification(user, status, action_status):
    subject = f"cinema - status update notification"
    message = f"""Dear {user},
     {'we are pleased ' if action_status == 'going_up' 
                        else 'it is with regret that we have'}
     to inform you that your status has been updated. 
     It is now {status}"""
    from_email = 'wukelan.yalishanda@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list,)


from django.core.mail import send_mail
from django.template.loader import get_template

def send_confirmation_email(email, token_id, user_id):
    data = {
        'token_id': str(token_id),
        'user_id' : str(user_id)
    }
    message = get_template('confirmation_email.txt').render(data)
    send_mail(subject='Please, confirm email',
              message=message,
              from_email='paglaumdaoback@hotmail.com',
              recipient_list=[email],
              fail_silently=True,
    )

class GhostUserClass:
    is_staff = False
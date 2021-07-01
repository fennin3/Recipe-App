import random
from django.core.mail import send_mail



def sending_mail(message,subject, email):
    send_mail(
        subject=subject,
        message=message,
        from_email= 'rennintech.com',
        recipient_list=[email],
        fail_silently=False,
    )


def generate_OTP():
    a = random.randint(000000, 999999)
    print(a)

    return a

# def send_sms(message):
#     client = rest.Client(cd.account_sid, cd.auth_token)

#     my_msg = message

#     message = client.messages.create(to=cd.my_cell, from_=cd.my_twilio,  body=my_msg)
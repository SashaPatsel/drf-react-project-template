# from django.contrib.staticfiles.templatetags.staticfiles import static
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from .serializers import AccountSerializer
from .models import Account

def get_default_img():
    images = ["prof_pics/prof1.jpg", "prof_pics/prof2.jpg", "prof_pics/prof3.jpg", "prof_pics/prof4.jpg", "prof_pics/prof5.jpg", "prof_pics/prof6.jpg", "prof_pics/prof7.jpg", "prof_pics/prof8.jpg", "prof_pics/prof9.jpg", "prof_pics/prof10.jpg", "prof_pics/prof11.jpg", "prof_pics/prof12.jpg", "prof_pics/prof13.jpg", "prof_pics/prof14.jpg", "prof_pics/prof15.jpg"]
    random_num = random.randint(0,14)
    return images[random_num]

def email_notification(account, message, link):
    if account.email_subscribed:
        subject = 'A notification from conservationist.io'
        from_email = settings.EMAIL_HOST_USER
        to_list = [account.user.email, settings.EMAIL_HOST_USER]
        htmly = get_template("email/notification.html")
        link = f"{settings.BASE_URL}{link}"
        context = { 
            "message": message,
            "link": link
            }
        html_content = htmly.render(context)
        plaintext = get_template("email/notification.html")
        text_content = plaintext.render(context)
        msg = EmailMultiAlternatives(subject, html_content, from_email, to_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        pass

def guest_email(email, message, link):
    subject = 'A notification from conservationist.io'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email, settings.EMAIL_HOST_USER]
    htmly = get_template("email/notification.html")
    link = f"{settings.BASE_URL}{link}"
    context = { 
        "message": message,
        "link": link
        }
    html_content = htmly.render(context)
    plaintext = get_template("email/notification.html")
    text_content = plaintext.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
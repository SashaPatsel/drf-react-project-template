import re 
from django.core.mail import EmailMultiAlternatives, send_mail
import os
  
def check_valid_email(email):  
    """
    Given a string, this function returns true if the string is an email, and false if it isnt.  
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex,email)):  
      return True
    else:  
      return False

def email_notification(user, message, link):
    subject = 'A notification from conservationist.io'
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]
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

def send_email(subject, message, to_email):
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  BASE_DIR = BASE_DIR[:-7]
  path = os.path.join(BASE_DIR, "templates", "email", "email.html")
  final_email = ""
  with open(path, "r+") as file:
    whole_message = file.read()
    email_parts = whole_message.split("split")
    final_email = message.join(email_parts)
  send_mail(
    subject,
    message,
    "spatsel.cci@gmail.com",
    to_email,
    fail_silently=False,
    html_message=final_email
  )
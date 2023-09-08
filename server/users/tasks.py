from apis.celery import app
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_verification_email(user_email , user_id , otp):
    subject = 'Verification Email'
    message = 'Please enable HTML in your email client to view this message.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    # Load and render the HTML email template
    html_message = render_to_string('emails/verification.html', context={"user_id": user_id, "otp": otp})
    
    # Send the email
    send_mail(subject, message, from_email, recipient_list, html_message=html_message , fail_silently=False)
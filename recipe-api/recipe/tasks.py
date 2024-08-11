from celery import shared_task;
from django.core.mail import send_mail;



@shared_task
def send_mail_when_liked(sendToList):
    send_mail("Your recepy has been liked", "recepy liked by someone",None,sendToList,fail_silently=False)
    return None

@shared_task
def send_mail_when_disliked(sendToList):
    send_mail("Your recepy has been disLiked", "recepy disLiked by someone",None,sendToList,fail_silently=False)
    return None
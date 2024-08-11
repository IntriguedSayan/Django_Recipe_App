from django.core.mail import send_mail;
from .serializers import RecipeSerializer;



def send_mail_when_liked_without_celery(title, message,sendToList):
    send_mail(title, message,None,sendToList,fail_silently=False)
    return None

def get_author_email_from_recipe(id):
    authorEmail=RecipeSerializer().get_author_email(id);
    return authorEmail;
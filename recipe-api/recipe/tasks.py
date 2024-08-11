from celery import shared_task;
from django.core.mail import send_mail;
from django.utils import timezone;
from datetime import timedelta;
from .models import Recipe,RecipeLike;


@shared_task
def send_mail_when_liked(sendToList):
    send_mail("Your recepy has been liked", "recepy liked by someone",None,sendToList,fail_silently=False)
    return None

@shared_task
def send_mail_when_disliked(sendToList):
    send_mail("Your recepy has been disLiked", "recepy disLiked by someone",None,sendToList,fail_silently=False)
    return None

@shared_task
def send_timely_like_notifications():
    one_hour_ago = timezone.now()-timedelta(hours=1)
    
    recent_likes = RecipeLike.objects.filter(created_gte=one_hour_ago);
    
    author_likes = {};
    for like in recent_likes:
        if(like.recipe.author in author_likes):
            author_likes[like.recipe.author].append(like.recipe)
        else:
            author_likes[like.recipe.author] = [like.recipe]
            
    for author, recipes in author_likes.items():
        recipe_titles = ", ".join([recipe.title for recipe in recipes])
        send_mail(
                 "Your recipes have been liked!",
                  f"The following recipes have been liked in the past hour: {recipe_titles}",None,
                  [author.email], fail_silently=False
                  )
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly
from .helpers import get_author_email_from_recipe, RecipePagination;
from .tasks import send_mail_when_liked,send_mail_when_disliked;
       

class RecipeListAPIView(generics.ListAPIView):
    """
    Get: a collection of recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    filterset_fields = ('category__name', 'author__username')
    pagination_class = RecipePagination

class RecipeCreateAPIView(generics.CreateAPIView):
    """
    Create: a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        authorEmail = get_author_email_from_recipe(get_object_or_404(Recipe, id=self.kwargs['pk']))
        new_like, created = RecipeLike.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        # print(new_like,created);
        if created:
            send_mail_when_liked.delay([authorEmail]);
            new_like.save()     
            return Response({"message":"Recipe liked successfully"},status=status.HTTP_201_CREATED)
        
        return Response({"message":"Recipe is already liked by you"},status=status.HTTP_200_OK)


    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        authorEmail = get_author_email_from_recipe(get_object_or_404(Recipe, id=self.kwargs['pk']))
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            send_mail_when_disliked.delay([authorEmail])
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """ Base class for tags and ingredients """
    authentication_classes = (TokenAuthentication,)  # this and
    permission_classes = (IsAuthenticated,)          # this
    #  forces the view viewer to be authenticated

    def get_queryset(self):
        """ Return the objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new object"""
        serializer.save(user=self.request.user)

    class Meta:
        abstract = True


class TagViewSet(BaseViewSet):
    """ Manage tags in the database """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseViewSet):
    """ Manage tags in the database """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return the objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return the proper serializer depending on the request """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

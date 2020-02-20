from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
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


class TagViewSet(BaseViewSet):
    """ Manage tags in the database """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseViewSet):
    """ Manage tags in the database """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

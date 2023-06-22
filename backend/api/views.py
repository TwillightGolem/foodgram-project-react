from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPaginator
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin
from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag
)
from .serializers import (
    AddRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShowRecipeSerializer,
    TagSerializer,
    ShowIngredientsInRecipeSerializer
)


class get_list_ingredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_classes = ShowIngredientsInRecipeSerializer

    def get_list_ingredients(user):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_recipe__user=user).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(amount=Sum('amount')).values_list(
                'ingredient__name', 'amount', 'ingredient__measurement_unit')
        return ingredients


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_classes = {
        'retrieve': ShowRecipeSerializer,
        'list': ShowRecipeSerializer,
    }
    default_serializer_class = AddRecipeSerializer
    permission_classes = (IsAuthorOrAdmin,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,
                                           self.default_serializer_class)

    def _favorite_shopping_post(self, related_manager):
        recipe = self.get_object()
        if related_manager.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже в избранном')
        related_manager.create(recipe=recipe)
        serializer = RecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _favorite_shopping_delete(self, related_manager):
        recipe = self.get_object()
        related_manager.get(recipe_id=recipe.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=('POST', 'DELETE',), )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._favorite_shopping_post(
                request.user.favorite
            )
        return self._favorite_shopping_delete(
            request.user.favorite
        )

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=('POST', 'DELETE',), )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self._favorite_shopping_post(
                request.user.shopping_user
            )
        return self._favorite_shopping_delete(
            request.user.shopping_user
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthorOrAdmin,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingList.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        buy_list = RecipeIngredient.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )

        buy_list_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in buy_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            buy_list_text += (
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )

        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )

        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter

from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def validate_username(self, username):
        cleaned_data = super().clean(self)
        curent_username = (User.objects.filter(
            username=cleaned_data.get('username')).exists())
        if username.lower() == 'me' or username == curent_username:
            raise serializers.ValidationError('Данное имя не доступно')
        elif username is None or username == '':
            raise serializers.ValidationError('Заполните имя')
        return username

    def clean(self):
        cleaned_data = super().clean(self)
        curent_email = cleaned_data.get('email').lower()
        if User.objects.filter(email=curent_email).exists():
            self.fields.add_error('email', "Эта почта уже зарегестрированна")
        return cleaned_data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (False if not request or request.user.is_anonymous
                else Follow.objects.filter(user=self.context['request'].user,
                                           author=obj).exists())


class FollowRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user and Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit_recipes = request.query_params.get('recipes_limit')
        if limit_recipes is not None:
            recipes = obj.recipes.all()[:(int(limit_recipes))]
        else:
            recipes = obj.recipes.all()
        context = {'request': request}
        return FollowRecipeSerializer(recipes, many=True,
                                      context=context).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()

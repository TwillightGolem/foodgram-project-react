from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionListView, follow_author

app_name = 'users'

api_router_v1 = DefaultRouter()
api_router_v1.register(
    r'users/subscriptions',
    SubscriptionListView,
    basename='subscriptions',
)

urlpatterns = [
    path('users/<int:pk>/subscribe/',
         follow_author,
         name='follow-author'),
    path(r'', include(api_router_v1.urls)),
]

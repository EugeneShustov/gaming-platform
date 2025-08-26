from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import GameViewSet, PostViewSet, game_detail_view, game_menu_view

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('game/<int:game_id>/', game_detail_view, name='game_detail'),
    path('', game_menu_view, name='game_menu'),
    path('api/', include(router.urls)),
]
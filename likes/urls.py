from django.urls import path, include
from .routers import CustomRouter
from .views import LikedItemViewSet

router = CustomRouter()
router.register('', LikedItemViewSet, basename="items")


urlpatterns = router.urls

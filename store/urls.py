from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'collections', views.CollectionViewSet, basename='collection')
router.register(r'reviews', views.ReviewViewSet, basename='collection')

urlpatterns = router.urls

from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'collections', views.CollectionViewSet, basename='collections')
router.register(r'carts', views.CartViewSet, basename='carts')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CardItemViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + carts_router.urls

from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'collections', views.CollectionViewSet, basename='collections')
router.register(r'carts', views.CartViewSet, basename='carts')
router.register(r'customers', views.CustomerViewSet, basename='customers')
router.register(r'orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CardItemViewSet, basename='cart-items')


urlpatterns = [
    path("test/", views.HelloView.as_view()),

] + router.urls + products_router.urls + carts_router.urls

from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    

    def get_total_price(self, card_item: CartItem):
        return card_item.quantity * card_item.product.unit_price
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class AddCardItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given product ID') 

    def save(self):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.filter(cart_id=cart_id, product_id=product_id).get()
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: CartItem):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()]) 

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    
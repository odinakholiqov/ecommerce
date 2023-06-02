from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    # viewing products
    # viewing product deetails
    # adding product to cart

    wait_time = between(1, 5) # 1 to 5 sec locust will wait

    @task(2)
    def view_products(self):
        collection_id = randint(2, 8)
        #sending request to prod endpoint
        self.client.get(f'/store/products/{collection_id}', name='/store/products')

    @task(4) # user is twice likely to execute below task rathen than the 1st one
    def view_product(self):
        product_id = randint(1, 30)
        self.client.get(f'/store/producs/{product_id}', name='/store/products/:id')

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/', 
            name='/store/carts/:id/items/',
            json={'product_id': product_id, 'quantity': 2}
        )

    # this get called every time when a new user starts browsing our web site
    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

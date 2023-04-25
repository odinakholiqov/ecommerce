from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Customer
from django.db.models import Count
def home(request):

    #product_list = Product.objects.all().order_by("title")
    product_list = Customer.objects.annotate(orders_count=Count('order'))
    
    
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get("page", 1)
    page_object = paginator.get_page(page_number)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2)
    
    return render(request, "store/home.html", {"page_object": page_object})

def search(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(title__icontains=query)

    paginator = Paginator(results, 4)
    page_number = request.GET.get("page", 1)
    page_object = paginator.get_page(page_number)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2)
    return render(request, "store/search.html", {"results": results, "page_object": page_object, "query": query})

def listing_api(request):
    page_number = request.GET.get("page", 1)   
    per_page = request.GET.get("per_page", 10)
    product = Product.objects.all().order_by("title")

    paginator = Paginator(product, per_page)
    page_obj = paginator.get_page(page_number)

    data = [{
        "title": kw.title,
        "description": kw.description,
        "unit_price": kw.unit_price
        } for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)
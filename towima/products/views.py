from django.shortcuts import render
from products.models import Category, Product

def products_list(request):
    products = Product.objects.all()
    args = {'products_list': products}
    return render(request, 'products/list.html', args)
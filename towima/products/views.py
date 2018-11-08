from django.shortcuts import render, get_object_or_404
from products.models import Category, Product

def products_list(request):
    products = Product.objects.all()
    args = {'products_list': products}
    return render(request, 'products/list.html', args)

def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    args = {'product': product,}
    return render(request, 'products/detail.html', args)
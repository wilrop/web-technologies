from django.shortcuts import render, get_object_or_404
from products.models import Category, Product
from pharmacies.models import Stock

def products_list(request):
    products = Product.objects.all()
    args = {'products_list': products}
    return render(request, 'products/list.html', args)

def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    entries = Stock.objects.filter(product=product.id)
    print(entries)
    args = {'product': product, 'entries': entries}
    return render(request, 'products/detail.html', args)
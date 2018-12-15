from django.shortcuts import render, get_object_or_404, redirect
from products.models import Category, Product
from pharmacies.models import Stock
from .forms import AddProductForm

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


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()   
            category = form.cleaned_data.get('category')
            name = form.cleaned_data.get('name')
            image = form.cleaned_data.get('image')
            description = form.cleaned_data.get('description')
            available = form.cleaned_data.get('available')
            return redirect('home')
    else:                                       
        form = AddProductForm()
    form = AddProductForm()
    return render(request, 'products/add_product.html', {'form': form})
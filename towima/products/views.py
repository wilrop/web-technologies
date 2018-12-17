from django.shortcuts import render, get_object_or_404, redirect
from products.models import Category, Product
from pharmacies.models import Stock
from accounts.models import Item, Cart
from .forms import AddtoCartForm, AddProductForm

def products_list(request):
    products = Product.objects.all()
    args = {'products_list': products}
    return render(request, 'products/list.html', args)

def product_detail(request, product_id, slug):  
    if request.method == 'POST':
        form = AddtoCartForm(request.POST, request.FILES)
        if form.is_valid():
            product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
            pharmacy = form.cleaned_data.get('pharmacy')
            quantity = form.cleaned_data.get('quantity')
            user = request.user
            cart = Cart.objects.get(user=user)
            stock = Stock.objects.get(product=product, pharmacy=pharmacy)
            unit_price = stock.product_price
            item = Item.objects.create(product=product, cart=cart, pharmacy=pharmacy, quantity=quantity, unit_price=unit_price)
            item.save()  
            return redirect('home')
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    entries = Stock.objects.filter(product=product.id)
    form = AddtoCartForm()
    args = {'product': product, 'entries': entries, 'form': form}
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
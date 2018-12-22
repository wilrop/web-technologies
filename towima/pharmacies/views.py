import time
import json
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from pharmacies.models import Pharmacy, Employee, Rating
from products.models import Product
from pharmacies.models import Stock
from pharmacies.forms import PharmacyForm, CommentForm, AddStockForm
from django.db.models import Q
from .forms import AddToCartForm
from accounts.models import Cart, Item
from mapbox import Geocoder
from orders.models import Order
from django.core.mail import send_mail

# The access token used for the Mapbox API.
mapbox_access_token = 'pk.eyJ1IjoibWF4aW1lYW50b2luZTE5OTciLCJhIjoiY2pubTNmNmlrMWpvdjNxdGFsdGxxaXJlayJ9.0tDqrdUlSYEOqxMSiy7j3g'

# The view that is created when requesting the profile of a pharmacy.
def pharmacy(request, pk):
    pharmacy = Pharmacy.objects.get(pk=pk)
    rated_list = Rating.objects.filter(pharmacy=pharmacy)       # Get the different ratings.
    pharmacy_stock = Stock.objects.filter(pharmacy=pharmacy)    # Get the stock.

    if rated_list:                  # Calculate the average rating and round this to an integer.
        acc_rating = 0
        for rating in rated_list:
            acc_rating += rating.rating
        rating = int(round(acc_rating / len(rated_list)))
    else:
        rating = None

    form = CommentForm             # We also include the comment form, so users can post comments on this page.
    args = {'pharmacy': pharmacy, 'rating': rating,
            'form': form, 'pharmacy_stock': pharmacy_stock}
    return render(request, 'pharmacies/pharmacy_profile.html', args)


def product_detail(request, pk, ppk):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=ppk)
            pharmacy = Pharmacy.objects.get(pk=pk)
            quantity = form.cleaned_data.get('quantity')
            user = request.user
            cart = Cart.objects.get(user=user)
            stock = Stock.objects.get(product=product, pharmacy=pharmacy)
            unit_price = stock.product_price
            item = Item.objects.create(
                product=product, cart=cart, pharmacy=pharmacy, quantity=quantity, unit_price=unit_price)
            item.save()
            return redirect('pharmacies:pharmacy', pk=pk) 
    pharmacy = Pharmacy.objects.get(pk=pk)
    product = Product.objects.get(pk=ppk)
    stock = Stock.objects.get(pharmacy=pharmacy, product=product)
    form = AddToCartForm()
    args = {'pharmacy': pharmacy, 'product': product,
            'stock': stock, 'form': form}
    return render(request, 'pharmacies/product_detail.html', args)


def create_pharma(request):
    if request.method == 'POST':                # When we POST the form.
        form = PharmacyForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            user = request.session['username']
            form.save(user)
    
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')

            pharmacy = Pharmacy.objects.get(name = name)
            pk = pharmacy.pk
            geocoder = Geocoder(access_token=mapbox_access_token)
            response = geocoder.forward(address)
            first = response.geojson()['features'][0]
            coords = [round(coord, 2)
                      for coord in first['geometry']['coordinates']]
            new_location = '{ "type": "Feature", "geometry": { "type": "Point", "coordinates": ' + str(coords) + '}, "properties": { "title": "' + name + '", "description": "' + str(pk) + '"}}'
            new_location = json.loads(new_location)

            file_path = os.path.join(settings.BASE_DIR, 'pharma_locations.json')
            
            pharma_locations = open(file_path)
            with pharma_locations as data_file:
                data = json.load(data_file)

            data["features"].append(new_location)

            pharma_locations = open(file_path, 'w')
            with pharma_locations as outfile:
                json.dump(data, outfile)
                
            return redirect('phone_verification')
    else:
        form = PharmacyForm()
    return render(request, 'pharmacies/create_pharmacy.html', {'form': form})


def add_comment_to_pharmacy(request):
    user = request.user
    author = user.username
    pharmacy = request.POST.get('pharmacy', None)
    text = request.POST.get('text', None)

    form = CommentForm({'text': text})
    if form.is_valid():
        valid = True
        comment = form.save(pharmacy, user)
        date = comment.created_date
    else:
        valid = False
        date = None

    data = {
        'valid': valid,
        'author': author,
        'text': text,
        'date': date,
    }
    return JsonResponse(data)


def add_rating_to_pharmacy(request):
    pk = request.GET.get('pk', None)
    new_rating = int(request.GET.get('new_rating', None))
    pharmacy = Pharmacy.objects.get(pk=pk)
    user = request.user

    rated_list = Rating.objects.filter(pharmacy=pharmacy)
    acc_rating = 0

    if rated_list:
        for rating in rated_list:
            acc_rating += rating.rating
        old_rating = int(round(acc_rating / len(rated_list)))
    else:
        old_rating = 1

    try:
        rating = Rating.objects.get(pharmacy=pharmacy, user=user)
        previous_rating = rating.rating
        rating.rating = new_rating
        new_rating = int(
            round((acc_rating - previous_rating + new_rating)/len(rated_list)))
    except Rating.DoesNotExist:
        rating = Rating(user=user, pharmacy=pharmacy, rating=new_rating)
        new_rating = int(
            round((acc_rating + new_rating)/(len(rated_list) + 1)))
    rating.save()

    data = {
        'old_rating': old_rating,
        'new_rating': new_rating
    }
    return JsonResponse(data)

# This view is utilized when a user searches something on the website.
def search(request):
    start = time.time()             # We compute the time spent searching.
    query = request.GET.get('q')
    results = []
    if query:
        results = Pharmacy.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query))     # Get all the results that match the query in the correct attributes.

    end = time.time()
    processing_time = format((end - start), '.4f')
    num_results = len(results)
    args = {'results': results, 'query': query,
            'time': processing_time, 'num_results': num_results}
    return render(request, 'pharmacies/search.html', args)

# This view responds with JSON data. The JSON is recieved from a local file with all the locations of pharmacies.
def get_locations(request):
    file_path = os.path.join(settings.BASE_DIR, 'pharma_locations.json') # Open the file on the correct path.
    pharma_locations = open(file_path)
    with pharma_locations as data_file:
        data = json.load(data_file)
    return JsonResponse(data)

# Definition of the view to show the settings for a pharmacy.
def pharma_settings(request):
    template = "pharmacies/pharma_settings.html"
    context = {}
    return render(request, template, context)

# definition of the view to display all the orders of a pharmacy.
def pharmacy_orders(request):
    template = 'pharmacies/orders.html'
    user = request.user
    pharmacy = Pharmacy.objects.get(owner=user)
    orders = Order.objects.filter(pharmacy=pharmacy)
    args = {'user': user, 'orders':orders}   
    return render(request, template, args)

# Definition of a view for the button on the orders page of a pharmacy to delete an order.
def order_delete(request, pk):
    order = Order.objects.get(pk=pk) 
    order.delete()
    return redirect(request.META['HTTP_REFERER'])

# Definition of a view for the button on the orders page of a pharmacy to fill an order.
def confirm_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.filled = True
    order.save()
    send_mail('Your order is ready!', 'Your order is ready in your local pharmacy!', 'pharmatowi@gmail.com', [getattr(order, 'email')], fail_silently=False,)
    return redirect(request.META['HTTP_REFERER'])

# Definition of a view to add a product to a pharmacy.
def add_product(request):
    user = request.user
    pharmacy = Pharmacy.objects.get(owner=user)
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            form.save(pharmacy)
            return redirect('home')
    form = AddStockForm()
    args = {'pharmacy': pharmacy, 'form': form}
    return render(request, 'pharmacies/add_product.html', args)
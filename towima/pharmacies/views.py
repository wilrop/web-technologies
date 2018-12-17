import time
import json
import os

from django.conf import settings
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from pharmacies.models import Pharmacy, Employee, Rating
from products.models import Product
from pharmacies.models import Stock
from pharmacies.forms import PharmacyForm, CommentForm
from django.db.models import Q
from .forms import AddToCartForm
from accounts.models import Cart, Item
from mapbox import Geocoder

mapbox_access_token = 'pk.eyJ1IjoibWF4aW1lYW50b2luZTE5OTciLCJhIjoiY2pubTNmNmlrMWpvdjNxdGFsdGxxaXJlayJ9.0tDqrdUlSYEOqxMSiy7j3g'


def pharmacy(request, pk):
    pharmacy = Pharmacy.objects.get(pk=pk)
    rated_list = Rating.objects.filter(pharmacy=pharmacy)
    pharmacy_stock = Stock.objects.filter(pharmacy=pharmacy)

    if rated_list:
        acc_rating = 0
        for rating in rated_list:
            acc_rating += rating.rating
        rating = int(round(acc_rating / len(rated_list)))
    else:
        rating = None

    form = CommentForm
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
            return redirect('home')
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
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')

            geocoder = Geocoder(access_token=mapbox_access_token)
            response = geocoder.forward(address)
            first = response.geojson()['features'][0]
            coords = [round(coord, 2)
                      for coord in first['geometry']['coordinates']]
            new_location = '{ "type": "Feature", "geometry": { "type": "Point", "coordinates": ' + str(coords) + '}, "properties": { "title": "' + name + '", "description": "' + phone_number +'"}}'
            new_location = json.loads(new_location)

            file_path = os.path.join(settings.BASE_DIR, 'pharma_locations.json')
            
            pharma_locations = open(file_path)
            with pharma_locations as data_file:
                data = json.load(data_file)

            data["features"].append(new_location)

            pharma_locations = open(file_path, 'w')
            with pharma_locations as outfile:
                json.dump(data, outfile)
                
            form.save()
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


def search(request):
    start = time.time()
    query = request.GET.get('q')
    results = []
    if query:
        results = Pharmacy.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query))

    end = time.time()
    processing_time = format((end - start), '.4f')
    num_results = len(results)
    args = {'results': results, 'query': query,
            'time': processing_time, 'num_results': num_results}
    return render(request, 'pharmacies/search.html', args)


def find_pharma(request):
    return render(request, 'pharmacies/find_pharma.html', {'mapbox_access_token': mapbox_access_token})


def get_locations(request):
    file_path = os.path.join(settings.BASE_DIR, 'pharma_locations.json')
    pharma_locations = open(file_path)
    with pharma_locations as data_file:
        data = json.load(data_file)
    return JsonResponse(data)


def pharma_settings(request):
    template = "pharmacies/pharma_settings.html"
    context = {}
    return render(request, template, context)

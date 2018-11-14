from django.shortcuts import render, get_object_or_404
from pharmacies.models import Pharmacy

def pharmacy_detail(request, pharmacy_id, slug):
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id, slug=slug, available=True)
    args = {'pharmacy': pharmacy,}
    return render(request, 'pharmacy/detail.html', args)

from django.shortcuts import render, redirect

def pharmacists_list(request):
    args = {'user': request.user}
    return render(request, 'pharmacists/list.html', args)
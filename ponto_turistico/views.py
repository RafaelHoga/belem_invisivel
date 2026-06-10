from django.shortcuts import render

# Create your views here.

def hotel_ibis(request):
    return render(request, 'hoteis/tela-hotel-ibis.html')

def utinga(request):
    return render(request, 'lugares_turisticos/tela-utinga.html')
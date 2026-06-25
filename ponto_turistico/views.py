from django.shortcuts import render

# Telas Principais / Listagens
def tela_turismo(request):
    return render(request, 'tela-turismo.html')

def tela_hoteis(request):
    return render(request, 'tela-hoteis.html')

def tela_restaurantes(request):
    return render(request, 'tela-restaurante.html') # Nome do seu template original

# Telas de Detalhes
def hotel_ibis(request):
    return render(request, 'hoteis/tela-hotel-ibis.html')
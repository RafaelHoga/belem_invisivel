from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PontoTuristico, Categoria

# ==========================================
# VIEWS PÚBLICAS DO SITE
# ==========================================

def tela_turismo(request):
    """Exibe a página pública com a listagem de Pontos Turísticos"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Turismo")
    return render(request, 'usuario/tela_turismo.html', {'locais': locais})


def tela_hoteis(request):
    """Exibe a página pública com a listagem de Hotéis"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Hotel")
    return render(request, 'usuario/tela_hoteis.html', {'locais': locais})


def tela_restaurante(request):
    """Exibe a página pública com a listagem de Restaurantes"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Restaurante")
    return render(request, 'usuario/tela_restaurante.html', {'locais': locais})


# ==========================================
# VIEWS ADMINISTRATIVAS (CRUD)
# ==========================================

def salvar_local(request, id_ponto=None):
    """Cria ou atualiza qualquer Ponto Turístico, Hotel ou Restaurante"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto) if id_ponto else None

    if request.method == 'POST':
        nome = request.POST.get('nome_ponto_turistico')
        telefone = request.POST.get('telefone')
        descricao = request.POST.get('descricao')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade', 'Belém')
        imagem_url = request.POST.get('imagem_url')
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        horario = request.POST.get('horario_funcionamento')
        id_categoria = request.POST.get('id_categoria')

        categoria_obj = get_object_or_404(Categoria, id_categoria=id_categoria)

        if ponto:
            ponto.nome_ponto_turistico = nome
            ponto.telefone = telefone
            ponto.descricao = descricao
            ponto.rua = rua
            ponto.bairro = bairro
            ponto.cidade = cidade
            ponto.imagem_url = imagem_url
            ponto.latitude = latitude
            ponto.longitude = longitude
            ponto.horario_funcionamento = horario
            ponto.categoria = categoria_obj
            ponto.save()
            messages.success(request, f'"{nome}" atualizado com sucesso!')
        else:
            PontoTuristico.objects.create(
                nome_ponto_turistico=nome,
                telefone=telefone,
                descricao=descricao,
                rua=rua,
                bairro=bairro,
                cidade=cidade,
                imagem_url=imagem_url,
                latitude=latitude,
                longitude=longitude,
                horario_funcionamento=horario,
                categoria=categoria_obj
            )
            messages.success(request, f'"{nome}" cadastrado com sucesso!')

    return redirect('usuario:painel_admin')


def excluir_local(request, id_ponto):
    """Remove permanentemente o local do banco de dados"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    if request.method == 'POST':
        ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
        nome = ponto.nome_ponto_turistico
        ponto.delete()
        messages.success(request, f'"{nome}" foi excluído com sucesso.')

    return redirect('usuario:painel_admin')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from .models import PontoTuristico, Categoria

# ==========================================
# FUNÇÃO AUXILIAR (FAVORITOS DO USUÁRIO)
# ==========================================
def obter_favoritos_usuario(request):
    """Retorna uma lista de IDs de pontos turísticos favoritados pelo usuário logado"""
    if request.user.is_authenticated:
        id_do_usuario = request.user.id_usuario
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_ponto_turistico 
                FROM favorito 
                WHERE id_usuario = %s
            """, [id_do_usuario])
            return [row[0] for row in cursor.fetchall()]
    return []

# ==========================================
# VIEWS PÚBLICAS DO SITE
# ==========================================
def index(request):
    """Exibe a página inicial do site buscando todos os locais salvos no MySQL e favoritos"""
    locais = PontoTuristico.objects.select_related('categoria').all()
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais_cadastrados': locais,
        'favoritos_ids': favoritos_ids  # Agora a index reconhece os favoritos do usuário
    }
    return render(request, 'index.html', {'locais_cadastrados': locais})


def tela_turismo(request):
    """Exibe a página pública com a listagem de Pontos Turísticos"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria__icontains="turismo")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids if favoritos_ids else []
    }
    return render(request, 'usuario/tela-turismo.html', context)


def tela_hoteis(request):
    """Exibe a página pública com a listagem de Hotéis"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria__icontains="hotel")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-hoteis.html', context)


def tela_restaurante(request):
    """Exibe a página pública com a listagem de Restaurantes / Gastronomia"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria__icontains="gastronomia") | PontoTuristico.objects.filter(categoria__descricao_categoria__icontains="restaurante")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-restaurante.html', context)


def detalhe_local(request, id_ponto):
    """Exibe os detalhes específicos de um local dinamicamente"""
    local = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    favoritado = False
    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM favorito 
                WHERE id_usuario = %s AND id_ponto_turistico = %s
            """, [request.user.id_usuario, id_ponto])
            favoritado = cursor.fetchone() is not None

    context = {
        'local': local,
        'favoritado': favoritado
    }
    return render(request, 'usuario/detalhes-local.html', context)


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
        
        nova_imagem = request.FILES.get('imagem_url')
        
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
            ponto.cidade = cidade if cidade else 'Belém'
            
            if nova_imagem:
                ponto.imagem_url = nova_imagem
                
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
                imagem_url=nova_imagem,
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
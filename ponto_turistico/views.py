from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PontoTuristico, Categoria, Favorito
from django.contrib.auth.decorators import login_required

# ==========================================
# FUNÇÃO AUXILIAR (FAVORITOS DO USUÁRIO)
# ==========================================
def obter_favoritos_usuario(request):
    """Retorna uma lista de IDs de pontos turísticos favoritados pelo usuário logado usando ORM"""
    if request.user.is_authenticated:
        # Uso do ORM ao invés de SQL Bruto, retorna lista plana de IDs
        return list(Favorito.objects.filter(id_usuario=request.user).values_list('id_ponto_turistico_id', flat=True))
    return []
# ==========================================
# VIEWS PÚBLICAS DO SITE
# ==========================================

@require_POST
def alternar_favorito(request, id_ponto):
    """Adiciona ou remove o ponto turístico dos favoritos do usuário autenticado"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Você precisa estar logado para favoritar.'}, status=401)

    ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)

    try:
        # Substituído get_or_create por filter para ser imune a registros duplicados no banco
        favoritos_existentes = Favorito.objects.filter(id_usuario=request.user, id_ponto_turistico=ponto)
        
        if favoritos_existentes.exists():
            # Se já existe, deleta todas as ocorrências encontradas (limpa duplicidades antigas)
            favoritos_existentes.delete()
            return JsonResponse({'status': 'sucesso', 'favoritado': False}, status=200)
        
        # Se não existe, cria o favorito de forma segura
        Favorito.objects.create(id_usuario=request.user, id_ponto_turistico=ponto)
        return JsonResponse({'status': 'sucesso', 'favoritado': True}, status=200)

    except Exception as e:
        # Exibe o erro detalhado no terminal do VSCODE
        print(f"\n--- ERRO CRÍTICO NO BANCO DE DADOS: {e} ---\n")
        # Retorna o erro real para podermos visualizar o nome do campo ausente se o banco rejeitar
        return JsonResponse({'error': f'Erro interno no banco: {str(e)}'}, status=500)
    
@login_required
def toggle_favorito(request, ponto_id):
    if request.method == "POST":
        try:
            ponto = PontoTuristico.objects.get(pk=ponto_id)
            # Verifica se já está favoritado por este usuário
            favorito_existente = Favorito.objects.filter(id_usuario=request.user, id_ponto_turistico=ponto)

            if favorito_existente.exists():
                favorito_existente.delete()
                return JsonResponse({'status': 'removido'})
            else:
                Favorito.objects.create(id_usuario=request.user, id_ponto_turistico=ponto)
                return JsonResponse({'status': 'adicionado'})
                
        except PontoTuristico.DoesNotExist:
            return JsonResponse({'error': 'Ponto turístico não encontrado'}, status=404)
            
    return JsonResponse({'error': 'Método inválido'}, status=400)

def tela_turismo(request):
    """Exibe a página pública com a listagem de Pontos Turísticos"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Turismo")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-turismo.html', context)


def tela_hoteis(request):
    """Exibe a página pública com a listagem de Hotéis"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Hotel")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-hoteis.html', context)


def tela_restaurante(request):
    """Exibe a página pública com a listagem de Restaurantes"""
    locais = PontoTuristico.objects.filter(categoria__descricao_categoria="Restaurante")
    favoritos_ids = obter_favoritos_usuario(request)
    
    context = {
        'locais': locais,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'usuario/tela-restaurante.html', context)


from django.http import JsonResponse  # Certifique-se de ter esse import no topo do arquivo

def detalhe_local(request, id_ponto):
    """Exibe os detalhes específicos de um local e processa suas avaliações de forma dinâmica"""
    local = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
    
    # 1. TRATAMENTO DO ENVIO DA AVALIAÇÃO VIA AJAX (POST)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Você precisa estar logado para avaliar.'}, status=403)

        nota = request.POST.get('nota_avaliacao')
        comentario = request.POST.get('comentario_texto')
        id_do_usuario = request.user.id_usuario 

        if not nota or not comentario or nota == '0':
            return JsonResponse({'error': 'Campos obrigatórios ausentes.'}, status=400)

        try:
            with connection.cursor() as cursor:
                # MUDANÇA AQUI: Removemos o SELECT e o UPDATE. Agora é SEMPRE INSERT direto!
                cursor.execute("""
                    INSERT INTO avaliacao (id_ponto_turistico, id_usuario, estrela, mensagem, data_avaliacao)
                    VALUES (%s, %s, %s, %s, NOW())
                """, [id_ponto, id_do_usuario, int(nota), comentario.strip()])
            
            return JsonResponse({'success': True}, status=200)
            
        except Exception as e:
            print(f"Erro ao salvar avaliação no MySQL: {e}")
            return JsonResponse({'error': f'Erro interno ao salvar no banco de dados: {str(e)}'}, status=500)

    # 2. SELEÇÃO DO TEMPLATE CORRETO COM BASE NO ID (GET)
    # =======================================================
    mapeamento_templates = {
        1: 'hoteis/tela-hotel-ibis.html',
        2: 'hoteis/tela-hotel-ipe.html',
        3: 'hoteis/tela-hotel-soft.html',
        4: 'Lugares_turisticos/lugares-pop/tela-estacao-docas.html',
        5: 'lugares_turisticos/lugares-pop/tela-ilha-de-cotijuba.html',
        6: 'lugares_turisticos/lugares-pop/tela-ilha-combu.html',
        7: 'restaurantes/tela-onze-janelas.html',
        8: 'restaurantes/tela-estilo-bistro.html',
        9: 'restaurantes/tela-familia.html',
        10: 'lugares_turisticos/lugares-inv/tela-palacete-bolonha.html',
        11: 'lugares_turisticos/lugares-inv/tela-caratateua.html',
        12: 'lugares_turisticos/lugares-inv/tela-trambioca.html',
        13: 'hoteis/tela-hotel-amazon.html',
        14: 'hoteis/tela-hotel-radisson.html',
        15: 'hoteis/tela-hotel-Atrium.html',
        16: 'hoteis/tela-hotel-transamerica.html',
        17: 'hoteis/tela-hotel-mercure.html',
    }

    template_escolhido = mapeamento_templates.get(id_ponto, 'usuario/detalhes-local.html')

    # Lógica de Favorito substituída pelo ORM do Django
    favoritado = False
    if request.user.is_authenticated:
        favoritado = Favorito.objects.filter(id_usuario=request.user, id_ponto_turistico=local).exists()

    context = {
        'local': local,
        'favoritado': favoritado
    }
    return render(request, template_escolhido, context)

def salvar_local(request, id_ponto=None):
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
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    if request.method == 'POST':
        ponto = get_object_or_404(PontoTuristico, id_ponto_turistico=id_ponto)
        nome = ponto.nome_ponto_turistico
        ponto.delete()
        messages.success(request, f'"{nome}" foi excluído com sucesso.')

    return redirect('usuario:painel_admin')


def excluir_avaliacao(request, id_ponto, id_usuario):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('usuario:login')

    if request.method == 'POST' or request.method == 'GET': 
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM avaliacao 
                WHERE id_ponto_turistico = %s AND id_usuario = %s
            """, [id_ponto, id_usuario])
        
        messages.success(request, 'Avaliação excluída com sucesso.')
    
    return redirect('usuario:painel_admin')


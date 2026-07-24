import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Sugestao
from ponto_turistico.models import Categoria


@login_required
@require_POST
def enviar_sugestao(request):
    """Recebe sugestão de ponto turístico (suporta AJAX/JSON e Form POST)"""
    try:
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'
        
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            nome = data.get('nome_sugestao')
            descricao = data.get('descricao', '')
            endereco = data.get('endereco')
            categoria_id = data.get('categoria')
        else:
            nome = request.POST.get('nome_sugestao')
            descricao = request.POST.get('descricao', '')
            endereco = request.POST.get('endereco')
            categoria_id = request.POST.get('categoria')
        
        if not nome or not endereco or not categoria_id:
            if is_ajax:
                return JsonResponse({'sucesso': False, 'erro': 'Campos obrigatórios ausentes.'}, status=400)
            messages.error(request, 'Campos obrigatórios ausentes.')
            return redirect('sugestao:sugestao_ponto_page')

        # Usa request.user diretamente (já autenticado pelo @login_required)
        categoria = Categoria.objects.get(pk=categoria_id)

        # Grava na tabela SUGESTAO do MySQL
        Sugestao.objects.create(
            nome_sugestao=nome,
            descricao=descricao,
            endereco=endereco,
            id_usuario=request.user,
            id_categoria=categoria
        )
        
        if is_ajax:
            return JsonResponse({'sucesso': True, 'mensagem': 'Sugestão enviada com sucesso! Ela passará por análise.'})
        
        messages.success(request, 'Sugestão enviada com sucesso! Ela passará por análise.')
        return redirect('sugestao:sugestao_ponto_page')
        
    except Categoria.DoesNotExist:
        if is_ajax:
            return JsonResponse({'sucesso': False, 'erro': 'Categoria inválida.'}, status=404)
        messages.error(request, 'Categoria inválida.')
        return redirect('sugestao:sugestao_ponto_page')
    except json.JSONDecodeError:
        return JsonResponse({'sucesso': False, 'erro': 'Formato JSON inválido.'}, status=400)
    except Exception as e:
        if is_ajax:
            return JsonResponse({'sucesso': False, 'erro': f'Erro interno no servidor: {str(e)}'}, status=500)
        messages.error(request, f'Erro interno no servidor: {str(e)}')
        return redirect('sugestao:sugestao_ponto_page')


@login_required
def sugestao_ponto_page(request):
    """Renderiza a página de sugestão de ponto turístico"""
    categorias = Categoria.objects.all()
    return render(request, 'sugestao_ponto.html', {'categorias': categorias})
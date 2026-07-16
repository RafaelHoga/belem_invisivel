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
    """Recebe sugestão de ponto turístico via AJAX (JSON)"""
    try:
        # Transforma o corpo do JSON enviado pelo JS em dicionário Python
        data = json.loads(request.body)
        
        nome = data.get('nome_sugestao')
        descricao = data.get('descricao', '')
        endereco = data.get('endereco')
        categoria_id = data.get('categoria')
        
        if not nome or not endereco or not categoria_id:
            return JsonResponse({'sucesso': False, 'erro': 'Campos obrigatórios ausentes.'}, status=400)

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
        
        return JsonResponse({'sucesso': True, 'mensagem': 'Sugestão enviada com sucesso! Ela passará por análise.'})
        
    except Categoria.DoesNotExist:
        return JsonResponse({'sucesso': False, 'erro': 'Categoria inválida.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'sucesso': False, 'erro': 'Formato JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'sucesso': False, 'erro': f'Erro interno no servidor: {str(e)}'}, status=500)


@login_required
def sugestao_ponto_page(request):
    """Renderiza a página de sugestão de ponto turístico"""
    categorias = Categoria.objects.all()
    return render(request, 'sugestao_ponto.html', {'categorias': categorias})
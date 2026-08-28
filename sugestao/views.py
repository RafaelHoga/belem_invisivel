from django.shortcuts import render
from django.http import JsonResponse
from .models import Sugestao
from ponto_turistico.models import Categoria
from usuario.models import Usuario

def enviar_sugestao(request):
    if request.method == 'POST':
        try:
            # Captura via POST e FILES (suporta envio simples ou via FormData no JS)
            nome = request.POST.get('nome_sugestao')
            descricao = request.POST.get('descricao', '')
            endereco = request.POST.get('endereco')
            categoria_id = request.POST.get('categoria')
            
            # CAPTURA DA FOTO ENVIADA
            imagem = request.FILES.get('imagem_ponto')
            
            # Recupera o usuário logado na sessão
            usuario_id = request.session.get('usuario_id') 

            if not usuario_id:
                return JsonResponse({'sucesso': False, 'erro': 'Você precisa estar logado para enviar uma sugestão.'}, status=403)

            if not nome or not endereco or not categoria_id:
                return JsonResponse({'sucesso': False, 'erro': 'Campos obrigatórios ausentes.'}, status=400)

            usuario = Usuario.objects.get(pk=usuario_id)
            categoria = Categoria.objects.get(pk=categoria_id)

            # Grava na tabela SUGESTAO (incluindo a imagem)
            Sugestao.objects.create(
                nome_sugestao=nome,
                descricao=descricao,
                endereco=endereco,
                id_usuario=usuario,
                id_categoria=categoria,
                imagem=imagem  # Certifique-se de que a model Sugestao possui este campo (ImageField)
            )
            
            return JsonResponse({'sucesso': True, 'mensagem': 'Sugestão enviada com sucesso! Ela passará por análise.'})
            
        except Usuario.DoesNotExist:
            return JsonResponse({'sucesso': False, 'erro': 'Usuário não encontrado.'}, status=404)
        except Categoria.DoesNotExist:
            return JsonResponse({'sucesso': False, 'erro': 'Categoria inválida.'}, status=404)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': f'Erro interno no servidor: {str(e)}'}, status=500)
            
    # Requisição GET: busca categorias e renderiza o HTML
    categorias = Categoria.objects.all()
    return render(request, 'sugestao_ponto.html', {'categorias': categorias})
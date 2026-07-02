from django.shortcuts import render, redirect
from .models import Sugestao, Usuario, Categoria

def salvar_sugestao(request):
    if request.method == "POST":

        nome = request.POST.get("nome_ponto_turistico")
        descricao = request.POST.get("descricao")
        categoria_id = request.POST.get("id_categoria")

        endereco = (
            f"{request.POST.get('endereco')}, "
            f"{request.POST.get('numero')} - "
            f"{request.POST.get('bairro')} - "
            f"{request.POST.get('cidade')}"
        )

        # usuario = Usuario.objects.get(
        #     id_usuario=request.session['id_usuario']
        # )

        usuario = Usuario.objects.get(id_usuario=1)
  
        categoria = Categoria.objects.get(
            id_categoria=categoria_id
        )

        Sugestao.objects.create(
            nome_sugestao=nome,
            descricao=descricao,
            endereco=endereco,
            usuario=usuario,
            categoria=categoria,
            status="Pendente"
        )

        return redirect('index')

    return render(request, 'sugestao.html')

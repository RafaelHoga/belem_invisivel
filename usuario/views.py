from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection  # Importante para rodar comandos SQL diretos no MySQL

# Buscando os modelos de seus respectivos apps corretos
from ponto_turistico.models import Favorito, Avaliacao
from usuario.models import Usuario
from sugestao.models import Sugestao

def home(request):
    return render(request, 'index.html')


# PERFIL ATUALIZADO PARA USAR A SESSÃO MANUAL
def perfil_usuario(request):
    # Se o ID do usuário não estiver na sessão, joga ele para a tela de login
    if 'usuario_id' not in request.session:
        messages.error(request, 'Por favor, faça o login para acessar o perfil.')
        return redirect('usuario:login')
        
    id_logado = request.session['usuario_id']
    
    meus_favoritos = Favorito.objects.filter(id_usuario=id_logado).select_related('id_ponto_turistico')
    minhas_sugestoes = Sugestao.objects.filter(id_usuario=id_logado)
    minhas_avaliacoes = Avaliacao.objects.filter(id_usuario=id_logado).select_related('id_ponto_turistico')
    
    context = {
        'favoritos': meus_favoritos,
        'sugestoes': minhas_sugestoes,
        'avaliacoes': minhas_avaliacoes,
    }
    
    return render(request, 'usuario/tela_perfil_usuario.html', context)


# FUNÇÃO DE CADASTRO COM SQL DIRETO
def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')
        senha = request.POST.get('senha_usuario')
        data_nasc = request.POST.get('data_nascimento')

        print("--- TENTATIVA COM SQL DIRETO ---")
        print(f"Nome: {nome} | Email: {email} | Data: {data_nasc}")

        if nome and email and senha and data_nasc:
            try:
                with connection.cursor() as cursor:
                    sql = """
                        INSERT INTO usuario (nome_usuario, email, senha, data_nascimento, id_perfil)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, [nome, email, senha, data_nasc, 2])
                
                print("SUCESSO ABSOLUTO: Inserido via SQL Direto!")
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('usuario:login')
                
            except Exception as e:
                print(f"ERRO DE BANCO DE DADOS DETECTADO: {e}")
                messages.error(request, f'Erro ao salvar no banco: {e}')
        else:
            print("AVISO: Algum campo obrigatório veio nulo do formulário HTML.")
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'usuario/tela-login.html')


# FUNÇÃO DE LOGIN COM REDIRECIONAMENTO SEGURO
def login_usuario(request):
    if request.method == 'POST':
        email_recebido = request.POST.get('email_usuario')
        senha_recebida = request.POST.get('senha_usuario')
        
        print("--- TENTATIVA DE LOGIN COM SQL DIRETO ---")
        print(f"Email: {email_recebido}")

        if email_recebido and senha_recebida:
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT id_usuario, nome_usuario, email FROM usuario WHERE email = %s AND senha = %s"
                    cursor.execute(sql, [email_recebido, senha_recebida])
                    usuario_encontrado = cursor.fetchone()

                if usuario_encontrado:
                    request.session['usuario_id'] = usuario_encontrado[0]
                    request.session['usuario_nome'] = usuario_encontrado[1]
                    request.session['usuario_email'] = usuario_encontrado[2]
                    
                    print(f"LOGIN EFETUADO: Bem-vindo {usuario_encontrado[1]}!")
                    messages.success(request, f'Bem-vindo de volta, {usuario_encontrado[1]}!')
                    
                    # Redirecionamento direto para a raiz do site '/' seguro
                    return redirect('/')  
                else:
                    print("AVISO: Credenciais incorretas no banco.")
                    messages.error(request, 'E-mail ou senha incorretos.')
                    
            except Exception as e:
                print(f"ERRO NO LOGIN (SQL): {e}")
                messages.error(request, f'Erro interno ao processar login: {e}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
            
    return render(request, 'usuario/tela-login.html')


# NOVA FUNÇÃO DE LOGOUT (LIMPA A SESSÃO MANUALMENTE)
def logout_usuario(request):
    print("--- ENCERRANDO SESSÃO DO USUÁRIO ---")
    request.session.flush()  # Destrói todas as variáveis de sessão salvas
    messages.success(request, 'Sessão encerrada com sucesso.')
    return redirect('/')
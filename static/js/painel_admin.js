/**
 * Alterna a visibilidade das abas internas do painel admin
 */
function alternarAba(abaId, menuId) {
    // Oculta todas as abas de conteúdo
    document.querySelectorAll('.aba-conteudo').forEach(aba => {
        aba.classList.remove('active');
        aba.style.display = 'none'; 
    });
    
    // Remove o destaque do menu lateral
    document.querySelectorAll('.sidebar-menu .menu-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Mostra e ativa a aba selecionada
    const abaSelecionada = document.getElementById(abaId);
    if (abaSelecionada) {
        abaSelecionada.classList.add('active');
        abaSelecionada.style.display = 'block'; 
    }
    
    // Ativa o destaque visual no menu lateral
    const menuSelecionado = document.getElementById(menuId);
    if (menuSelecionado) {
        menuSelecionado.classList.add('active');
    }
}

/**
 * Função global de filtragem para tabelas por id de categoria
 */
function filtrarPorCategoria(contexto, categoriaId) {
    const linhas = document.querySelectorAll(`.linha-filtravel-${contexto}`);
    linhas.forEach(linha => {
        if (categoriaId === 'todos' || linha.getAttribute('data-cat-id') === categoriaId) {
            linha.style.display = '';
        } else {
            linha.style.display = 'none';
        }
    });
}

/**
 * Controle do Modal de Locais (Pontos Turísticos, Hotéis, Restaurantes)
 */
function abrirModalCadastro(categoriaNome = "") {
    document.getElementById('modalTitulo').innerText = "Adicionar Novo Local";
    document.getElementById('formLocal').action = "/turismo/novo/"; 
    document.getElementById('formLocal').reset();

    if (categoriaNome) {
        const selectCategoria = document.getElementById('input_categoria');
        for (let i = 0; i < selectCategoria.options.length; i++) {
            if (selectCategoria.options[i].text.toLowerCase().includes(categoriaNome.toLowerCase())) {
                selectCategoria.selectedIndex = i;
                break;
            }
        }
    }
    document.getElementById('modalLocal').style.display = 'flex';
}

function abrirModalEditar(botao) {
    document.getElementById('modalTitulo').innerText = "Editar Local";
    
    // Recupera os dados guardados nos atributos data-* do botão clicado
    const id = botao.dataset.id;
    const nome = botao.dataset.nome;
    const telefone = botao.dataset.telefone;
    const idCategoria = botao.dataset.categoria;
    const descricao = botao.dataset.descricao;
    const rua = botao.dataset.rua;
    const bairro = botao.dataset.bairro;
    const cidade = botao.dataset.cidade;
    const horario = botao.dataset.horario;
    const latitude = botao.dataset.latitude;
    const longitude = botao.dataset.longitude;
    
    // Define a rota de action dinâmica do formulário de edição
    document.getElementById('formLocal').action = "/turismo/editar/" + id + "/";
    
    // Atribui os valores recuperados aos inputs do modal
    document.getElementById('input_nome').value = nome;
    document.getElementById('input_telefone').value = telefone;
    document.getElementById('input_categoria').value = idCategoria;
    document.getElementById('input_descricao').value = descricao;
    document.getElementById('input_rua').value = rua;
    document.getElementById('input_bairro').value = bairro;
    document.getElementById('input_cidade').value = cidade;
    document.getElementById('input_horario').value = horario;
    document.getElementById('input_latitude').value = latitude;
    document.getElementById('input_longitude').value = longitude;
    
    // Nota: inputs do tipo 'file' não podem receber valores de texto por segurança do navegador,
    // mas o formulário enviará o arquivo normalmente se o usuário selecionar um novo.
    document.getElementById('input_imagem').value = ""; 
    
    document.getElementById('modalLocal').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('modalLocal').style.display = 'none';
}

/**
 * Controle do Modal de Categorias (CRUD)
 */
function abrirModalCategoria() {
    document.getElementById('modalCategoriaTitulo').innerText = "Adicionar Nova Categoria";
    document.getElementById('formCategoria').action = "/usuario/painel/categoria/nova/";
    document.getElementById('formCategoria').reset();
    document.getElementById('modalCategoria').style.display = 'flex';
}

function abrirModalEditarCategoria(id, descricao) {
    document.getElementById('modalCategoriaTitulo').innerText = "Editar Categoria";
    document.getElementById('formCategoria').action = "/categoria/editar/" + id + "/";
    document.getElementById('input_nome_categoria').value = descricao;
    document.getElementById('modalCategoria').style.display = 'flex';
}

function fecharModalCategoria() {
    document.getElementById('modalCategoria').style.display = 'none';
}

/**
 * Inicialização do Painel
 */
document.addEventListener("DOMContentLoaded", function() {
    alternarAba('aba-dashboard', 'menu-dashboard');
});
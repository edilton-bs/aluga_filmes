// Função para listar filmes disponíveis automaticamente
async function listarFilmesDisponiveis() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/filmes-disponiveis');
        if (!response.ok) {
            throw new Error('Erro ao buscar filmes disponíveis!');
        }
        const filmes = await response.json();

        const filmesContainer = document.getElementById('filmes');
        filmesContainer.innerHTML = ''; // Limpa o contêiner antes de exibir

        filmes.forEach(filme => {
            const filmeElement = document.createElement('div');
            filmeElement.innerHTML = `
                <h3>${filme.titulo}</h3>
                <p>Gênero: ${filme.genero}</p>
                <p>Quantidade disponível: ${filme.quantidade_disponivel}</p>
                <button class="alugar-btn" data-id="${filme.id}" data-titulo="${filme.titulo}">Alugar</button>
            `;
            filmesContainer.appendChild(filmeElement);
        });

        // Adiciona eventos para todos os botões "Alugar"
        document.querySelectorAll('.alugar-btn').forEach(button => {
            button.addEventListener('click', (event) => {
                const filmeId = event.target.getAttribute('data-id');
                const filmeTitulo = event.target.getAttribute('data-titulo');
                abrirModalAluguel(filmeId, filmeTitulo);
            });
        });
    } catch (error) {
        console.error(error.message);
        const filmesContainer = document.getElementById('filmes');
        filmesContainer.innerHTML = `<p style="color: red;">${error.message}</p>`;
    }
}

async function abrirModalAluguel(filmeId, filmeTitulo) {
    const modal = document.getElementById('aluguel-modal');
    const modalTitulo = document.getElementById('modal-titulo');
    const modalFilmeId = document.getElementById('filme-id');
    const usuarioDropdown = document.getElementById('usuario');

    modalTitulo.textContent = `Alugar: ${filmeTitulo}`;
    modalFilmeId.value = filmeId;

    try {
        // Faz uma requisição para buscar os usuários
        const response = await fetch('http://127.0.0.1:5000/api/usuarios');
        if (!response.ok) {
            throw new Error('Erro ao buscar usuários!');
        }
        const usuarios = await response.json();

        // Preenche o dropdown com os usuários
        usuarioDropdown.innerHTML = ''; // Limpa as opções existentes
        usuarios.forEach(usuario => {
            const option = document.createElement('option');
            option.value = usuario.id;
            option.textContent = usuario.nome;
            usuarioDropdown.appendChild(option);
        });
    } catch (error) {
        console.error(error.message);
        usuarioDropdown.innerHTML = `<option value="">Erro ao carregar usuários</option>`;
    }

    modal.style.display = 'block'; // Mostra o modal
}

// Fechar o modal de aluguel
document.getElementById('fechar-modal').addEventListener('click', () => {
    document.getElementById('aluguel-modal').style.display = 'none';
});

// Executa a função automaticamente ao carregar a página
document.addEventListener('DOMContentLoaded', listarFilmesDisponiveis);







document.getElementById('form-aluguel').addEventListener('submit', async (event) => {
    event.preventDefault();

    const filmeId = document.getElementById('filme-id').value;
    const usuario = document.getElementById('usuario').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/alugar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filme_id: filmeId, usuario })
        });

        const result = await response.json();
        alert(result.message);

        // Fecha o modal e atualiza a lista de filmes disponíveis
        document.getElementById('aluguel-modal').style.display = 'none';
        listarFilmesDisponiveis();
    } catch (error) {
        alert('Erro ao realizar o aluguel!');
    }
});

document.getElementById('aluguel-modal').style.display = 'none';

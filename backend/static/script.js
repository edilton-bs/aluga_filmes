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
            `;
            filmesContainer.appendChild(filmeElement);
        });
    } catch (error) {
        console.error(error.message);
        const filmesContainer = document.getElementById('filmes');
        filmesContainer.innerHTML = `<p style="color: red;">${error.message}</p>`;
    }
}

// Executa a função automaticamente ao carregar a página
document.addEventListener('DOMContentLoaded', listarFilmesDisponiveis);

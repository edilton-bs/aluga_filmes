// Função para buscar e exibir os filmes
async function listarFilmes() {
    try {
        // Faz a requisição GET para o endpoint do backend
        const response = await fetch('http://127.0.0.1:5000/api/filmes');
        if (!response.ok) {
            throw new Error('Erro ao buscar filmes!');
        }
        const filmes = await response.json();

        // Seleciona o contêiner onde os filmes serão exibidos
        const filmesContainer = document.getElementById('filmes');

        // Limpa o contêiner antes de adicionar novos filmes
        filmesContainer.innerHTML = '';

        // Adiciona os filmes ao contêiner
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
    }
}

// Adiciona um evento de clique ao botão
document.getElementById('listar-filmes').addEventListener('click', listarFilmes);

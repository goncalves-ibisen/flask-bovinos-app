// Função para detectar pressionamento de tecla Enter e enviar a consulta
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Evita o comportamento padrão do Enter
        document.getElementById('search-form').submit(); // Envia o formulário automaticamente
    }
}

// Função para iniciar a pesquisa por voz
function startVoiceSearch() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'pt-BR';
        recognition.start();

        recognition.onresult = function(event) {
            const speechToText = event.results[0][0].transcript;
            document.getElementById('search-input').value = speechToText;
            document.getElementById('search-form').submit(); // Envia o formulário automaticamente após a transcrição
        };

        recognition.onerror = function(event) {
            console.error('Erro no reconhecimento de voz: ', event.error);
        };
    } else {
        alert('Seu navegador não suporta reconhecimento de voz.');
    }
}

// Função para formatar o campo 'valor'
function formatarValorAnimal() {
    const valorElement = document.getElementById('valor');
    if (valorElement) {
        const valor = parseFloat(valorElement.textContent);
        valorElement.textContent = `R$ ${isNaN(valor) ? '0,00' : valor.toFixed(2).replace('.', ',')}`;
    }
}

// Chama a função para formatar o valor ao carregar a página
window.onload = function() {
    formatarValorAnimal();
};

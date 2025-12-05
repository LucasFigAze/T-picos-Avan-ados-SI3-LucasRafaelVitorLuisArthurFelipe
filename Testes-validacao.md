# Canvas de Testes e Validação

## Descrição

Enquanto o `Canvas de Desenho de Experimento` valida a *hipótese de negócio*, o **Canvas de Testes e Validação** foca em verificar a *qualidade técnica da implementação*. Ele organiza e documenta os processos de testes do assistente inteligente, garantindo que as funcionalidades atendam aos requisitos especificados и que o sistema opere de forma confiável, segura e eficiente. Abrange testes funcionais, de desempenho, de segurança e de experiência do usuário, além de definir critérios de aceitação claros.

### 1. Objetivo dos Testes
- **Objetivo**: Garantir que o assistente inteligente consiga se conectar corretamente à API do Google Gemini, validar carregamento de variáveis de ambiente, configuração da SDK, instanciação do modelo e retorno de resposta a partir de um prompt simples. O objetivo é assegurar que a camada de integração está funcional e pronta para suportar fluxos mais complexos de negociação e tomada de decisão.

### 2. Tipos de Testes
- **Teste de Integração**: Validar a comunicação entre o sistema local e a API do Google Gemini.
- **Teste de Configuração/Ambiente**: Verificar a existência e leitura do arquivo .env.
- **Teste Funcional Básic**o**: Confirmar que o modelo responde corretamente a prompts simples.
- **Teste de Resiliência**: Capturar e interpretar erros de autenticação, conexão e indisponibilidade da API.
- **Teste de Dependências**: Verificar funcionamento das bibliotecas dotenv e google.generativeai

### 3. Casos de Teste
- **Caso 1:** 
  - Carregamento do .env
  - Entrada: Arquivo .env existente.
  - Ação: Executar o script.
  - Resultado Esperado: Mensagem “Arquivo .env carregado.”
- **Caso 2:** 
  - Chave de API presente
  - Entrada: Variável GOOGLE_API_KEY definida.
  - Ação: Executar o script.
  - Resultado Esperado: Mensagem “Chave de API carregada com sucesso.”
- **Caso 3:** 
  - Chave de API ausente
  - Entrada: .env sem a variável.
  - Ação: Executar o script.
  - Resultado Esperado: Mensagem de erro específica avisando que não foi encontrada.
- **Caso 4:** 
  - Chamada bem-sucedida ao Gemini
  - Entrada: Prompt “Qual é a capital do Brasil?”
  - Ação: Executar o método generate_content.
  - Resultado Esperado: Retorno textual do modelo e mensagem “TESTE BEM-SUCEDIDO!”.
- **Caso 5:** 
  - Falha na chamada à API
  - Entrada: Chave inválida / sem internet / API indisponível.
  - Ação: Executar script.
  - Resultado Esperado: Mensagem “TESTE FALHOU” + causas prováveis.

### 4. Critérios de Aceitação
- O script deve carregar corretamente a variável do .env.
- O SDK deve ser configurado sem erros.
- A chamada ao modelo deve retornar uma resposta válida.
- O sistema deve exibir mensagens amigáveis em caso de erro.
- Todo erro deve ser tratável pelo bloco except, sem travar a aplicação.

### 5. Ferramentas de Teste
- **Ferramentas**: Para realização dos testes utilizamos o python-dotenv e google-generativeai (SDK oficial Gemini)

### 6. Equipe e Responsabilidades
- **Equipe**: Os testes são feitos a cada iteração no código por todos os membros, já que as ferramentas automatizam.

### 7. Resultados e Relatórios
- **Resultados**: É possível acompanhar os resultados no código.

### 8. Planos de Reteste
- **Reteste**: A cada iteração realizamos novos testes automatizados.

### 9. Monitoramento Contínuo
- **Monitoramento**: Automatizar execução periódica do teste em pipeline.

### 10. Feedback e Iteração
- **Feedback**: Os feedbacks pegos serão adicionados ao Backlog da solução.
# Registro de Estratégia de Inteligência

A tabela abaixo detalha as decisões técnicas, a escolha de modelos e a estratégia de dados para o projeto.

| Componente | Decisão | Justificativa |
| :--- | :--- | :--- |
| **Abordagem Estratégica** | **RAG** (Retrieval-Augmented Generation) | Fine-tuning é desnecessário e perigoso aqui. Precisamos de precisão factual (valor da dívida, regras de desconto) que muda a cada cliente. [cite_start]O RAG injeta esses dados no contexto em tempo real, reduzindo alucinações.  |
| **Modelo Base (LLM)** | **Google Gemini 1.5 Flash** | [cite_start]Possui janela de contexto grande (para históricos longos de conversa), é rápido (baixa latência para chat) e custo-eficiente para escalar.  |
| **Memória** | **Conversation Buffer Window** | [cite_start]O sistema deve enviar as últimas X mensagens da troca para o modelo manter a coerência do diálogo ("Como eu disse antes...").  |
| **Dados** | **Estruturados (Inicialmente)** | No MVP, o contexto virá de queries SQL diretas (Tabelas de Clientes e Faturas). [cite_start]Na Fase 2, evoluirá para RAG Vetorial para ler PDFs de contratos.  |
| **Fallback** | **Human-in-the-Loop** | [cite_start]Se a IA detectar sentimento muito negativo ou o cliente pedir "falar com humano", o bot transfere o status para atendimento manual (previsto no roadmap).  |

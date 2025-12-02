# Checklist de Análise de Riscos e Defensabilidade em IA

## Descrição

Este artefato operacionaliza o pilar **Defensável**. Ele guia a equipe na identificação, avaliação e planejamento da mitigação de riscos relacionados à justiça, privacidade, segurança e transparência da solução. Não é apenas uma lista de verificação, mas uma ferramenta para fomentar a discussão crítica e registrar o compromisso da equipe com a construção de uma IA responsável.

### 1. Análise de Justiça e Viés (Fairness & Bias)

- **Risco Principal**:A IA pode oferecer condições diferentes de negociação dependendo de atributos correlacionados com raça, gênero, localidade, idade, ou mesmo uso de linguagem, o que reforça discriminação.
  - IA sugerindo negociações melhores ou piores dependendo do nome, idade, sotaque ou forma de escrita do paciente.
  - Ofertas consistentemente piores para grupos geográficos ou socioeconômicos.
  - Tratamento desigual entre clientes “mais comunicativos” vs. pacientes “objetivos”.

### 2. Análise de Privacidade e Dados

- **Risco Principal**: Exposição de dados financeiros sensíveis, uso além do consentido, ou re-identificação a partir de dados anonimizados.
  - Logs de conversa contendo CPF/CNPJ, números de conta ou documentos sem proteção.
  - Uso indevido de dados históricos para treinar modelos sem consentimento.
  - Retenção indefinida de gravações de negociação.

### 3. Análise de Segurança e Robustez

- **Risco Principal**: Manipulação do modelo, via promp injection, exploração de lógica de negociação, ou abuso para extrair dados de outros clientes / manipular termos.
  - Clientes tentam forçar a IA a ignorar regras e oferecer mais desconto (prompt injection).
  - Atacantes tentando extrair dados via engenharia de prompts (data exfiltration).
  - Automação aprovando acordos fora de limites comerciais (fuga de regras).

### 4. Análise de Transparência e Explicabilidade

- **Risco Principal**: Cliente ou analista não entender por que a IA sugeriu X termos, levando a desconfiança ou disputa legal.
  - Resposta sem justificativa ("oferta: parcelar em 6x") sem explicar critérios.
  - Falta de aviso claro de que a contraparte é uma IA.
  - Decisões automatizadas sem registro do critério usado.

### 5. Matriz de Priorização de Riscos

- **Crítico(prioritário)**: 
  - Vazamento de dados sensíveis.
  - IA finalizando acordos fora de política.
  - Prompt injection levando a concessões indevidas.
  - Linguagem hostíl da IA.
- **Risco Alto**: 
  - Decisões enviesadas por descriminação.
  - Model hallucination com termos incorretos.
- **Cuidado**: 
  - Erros operacionais (timeouts)
  - Problemas de UX


### 6. Plano de Mitigação

- **Crítico(prioritário)**: 
  - Vazamento de dados sensíveis - seguir regras da LGPD, anonimação de dados e criptografia.
  - IA finalizando acordos fora de política - Definir limites inicialmente, junto com validação através do HITL 
  - Prompt injection levando a concessões indevidas - Camada pré-modelo: detector de intent malicios
  - Linguagem hostíl da IA - Auditoria de conversas e treinamento com banco de dados neutro da LLM.
- **Risco Alto**: 
  - Decisões enviesadas por descriminação - Remover proxies sensíveis; aplicar fairness-aware training e constraints.
  - Model hallucination com termos incorretos - Fonte única de verdade (single source of truth) para regras comerciais — a IA consulta o back-end, não “lembra” de cabeça.
- **Cuidado**: 
  - Erros operacionais (timeouts) - Monitoramento contínuo e testes frequentes.
  - Problemas de UX - Entrevistas para entendimento e evolução junto aos usuários.
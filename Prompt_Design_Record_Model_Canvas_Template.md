# 📄 Registro de Design de Prompt: COBRANCA-PERSONALIZADA-01

## 1. Metadados
**Propósito:**  
Gerar uma mensagem personalizada de cobrança amigável, adaptada ao perfil e histórico do cliente, com o objetivo de estimular o pagamento espontâneo, evitando a necessidade de intervenção humana.

**Modelo(s) Alvo:**  
OpenAI GPT-4 / GPT-4o

**Versão do Registro:**  
1.0

---

## 2. Estrutura do Prompt

**Contexto de Entrada Necessário:**
- Nome do cliente
- Valor da dívida
- Data de vencimento original
- Tempo de atraso (em dias)
- Histórico de pagamento (ex: bom pagador, inadimplente frequente, primeiro atraso etc.)
- Canal de contato preferencial (ex: WhatsApp, e-mail, SMS)
- Política de cobrança (ex: aplicar juros? desconto para pagamento imediato?)
- Grau de severidade da comunicação (leve, moderada, urgente)

**Template do Prompt (com variáveis):**
```
Você é um assistente virtual de atendimento ao cliente especializado em negociações amigáveis de cobrança. Seu objetivo é redigir uma mensagem personalizada, empática e clara para incentivar o pagamento de uma dívida em aberto.

Informações do cliente:
- Nome: {nome_cliente}
- Valor da dívida: R$ {valor_divida}
- Dias de atraso: {dias_atraso}
- Histórico de pagamento: {historico_pagamento}
- Canal de contato: {canal_contato}
- Política de cobrança: {politica_cobranca}
- Grau de severidade da mensagem: {grau_severidade}

Gere uma mensagem curta (máx. 500 caracteres), com tom apropriado ao canal, levando em consideração o perfil do cliente e o grau de urgência. A mensagem deve ser empática, oferecer opções quando possível, e evitar linguagem agressiva. Inicie com o nome do cliente e use linguagem natural.

Apenas a mensagem, sem explicações ou formatação adicional.
```

---

## 3. Estrutura da Resposta

**Intenção da Resposta:**  
Mensagem de texto curta e direta, com tom humano e empático, adaptada ao perfil do cliente e ao canal de comunicação.

**Exemplo de Saída Ideal:**
```
Oi João, tudo bem? Notamos que o pagamento de R$ 279,90, vencido em 12/09, ainda está pendente. Sabemos que imprevistos acontecem, e estamos aqui para ajudar. Se preferir, podemos negociar ou prorrogar a data. Fale com a gente por aqui mesmo. 😊
```

---

## 4. Teste e Qualidade

**Critérios de Aceite / Métricas de Qualidade:**
- ✅ A mensagem deve conter o nome do cliente.
- ✅ Deve mencionar o valor da dívida e o vencimento (direta ou indiretamente).
- ✅ O tom deve ser adequado ao canal e grau de severidade.
- ✅ Não pode ser ameaçador, invasivo ou usar linguagem jurídica.
- ✅ Deve caber em até 500 caracteres (para compatibilidade com WhatsApp e SMS).
- ✅ Pode sugerir negociação, parcelamento ou contato.
- ✅ Não deve conter links (a menos que explicitamente autorizado).

**Parâmetros Recomendados:**
- Temperatura: `0.7` (para respostas com leve personalização e criatividade controlada)
- Top-p: `0.9`
- Max tokens: `250` (output)

---

## 5. Notas Adicionais

**Instruções:**
- Ideal usar um motor de decisão antes do prompt para classificar o tipo de cliente (bom pagador, reincidente, etc.), o que ajusta a variável `{grau_severidade}`.
- Pode ser útil criar templates diferentes por canal (ex: WhatsApp = informal, e-mail = mais formal).
- Testes mostraram que mensagens com emojis e tom positivo têm maior taxa de resposta no WhatsApp.
- Considerar testes A/B com diferentes versões da mensagem para medir eficácia.
- **LGPD:** Certifique-se de que o uso de dados pessoais esteja em conformidade com a legislação vigente.

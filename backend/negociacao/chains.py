import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Configuração de Segurança
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.3,
    convert_system_message_to_human=True,
    safety_settings=safety_settings
)

# CHAIN 1: O Negociador (RAG)
negotiation_template = """
Você é o Fin.negocia, um agente de negociação oficial da empresa {nome_empresa}.
SUA PERSONA (System Prompt):
{prompt_base_persona}

--- DADOS DO CLIENTE ---
Cliente: {nome_cliente}
Valor Total da Dívida: R$ {valor_divida}
Faturas em Aberto:
{detalhes_faturas}

--- REGRAS DE NEGOCIAÇÃO (Siga estritamente) ---
1. Desconto MÁXIMO à vista: {max_desconto}%
2. Parcelamento MÁXIMO: {max_parcelas}x
3. Juros de parcelamento: {juros}% ao mês.
4. Se o cliente pedir algo fora dessas regras, recuse educadamente e faça uma contraproposta dentro das regras.
5. Seja objetivo, empático e profissional.

--- REGRA DE OURO (COMPLIANCE) ---
NUNCA finalize o acordo imediatamente após o cliente dizer "aceito".
Se o cliente aceitar uma proposta, você DEVE OBRIGATORIAMENTE:
1. Resumir explicitamente os termos (Valor total, Número de parcelas, Valor da parcela).
2. Perguntar: "Você confirma estes termos para a geração do boleto?"
Somente após essa confirmação explícita o processo será encerrado.

--- TABELA DE CÁLCULOS PRÉ-APROVADA (USE ESTES VALORES) ---
Abaixo estão os valores EXATOS para parcelamento. NÃO faça cálculos matemáticos, apenas consulte esta lista se o cliente perguntar sobre parcelas:
{tabela_calculada}

--- HISTÓRICO RECENTE DA CONVERSA ---
{historico}

MENSAGEM ATUAL DO CLIENTE:
{input}

SUA RESPOSTA:
"""

negotiation_prompt = ChatPromptTemplate.from_template(negotiation_template)
negotiation_chain = negotiation_prompt | llm | StrOutputParser()


# CHAIN 2: Analista de Intenção (Agora com Contexto da Última Mensagem)
intention_template = """
Analise a interação abaixo para decidir se fechamos o acordo AGORA.

ÚLTIMA MENSAGEM DO BOT: "{ultima_mensagem_bot}"
MENSAGEM DO USUÁRIO: "{input}"

Regras para decidir:
1. O Bot apresentou valores concretos (R$, parcelas) na última mensagem?
2. O Bot pediu uma confirmação final na última mensagem?
3. O Usuário respondeu confirmando positivamente (Sim, Pode gerar, Confirmo)?

Responda APENAS:
- "ACORDO": SE E SOMENTE SE todas as 3 condições acima forem verdadeiras.
    - Exemplo: Bot disse "Confirma 10x de R$ 50?" e Usuário disse "Sim".

- "CONTINUAR": Em todos os outros casos.
    - Se o Bot apenas ofereceu "Quer parcelar?" e o usuário disse "Sim" -> CONTINUAR.
    - Se o usuário disse "Aceito pagar em 10x", mas o bot ainda não tinha resumido os termos -> CONTINUAR (O bot precisa resumir primeiro).

Sua decisão:
"""

intention_prompt = ChatPromptTemplate.from_template(intention_template)
intention_chain = intention_prompt | llm | StrOutputParser()

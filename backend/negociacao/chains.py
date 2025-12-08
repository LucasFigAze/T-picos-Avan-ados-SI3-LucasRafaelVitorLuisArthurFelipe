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
    temperature=0.5,
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


# CHAIN 2: Analista de Intenção
intention_template = """
Analise a última mensagem do usuário. O objetivo é identificar se a negociação foi CONCLUÍDA e o acordo pode ser registrado AGORA.

Responda APENAS:
- "ACORDO": SOMENTE se o usuário concordou explicitamente com uma proposta JÁ FEITA pelo bot.
    - Exemplos Válidos: "Pode gerar o boleto", "Fechado", "Aceito", "Pode mandar".
    
- "CONTINUAR": Em qualquer outro caso, inclusive se o usuário sugerir novos termos.
    - Se o usuário disser "Faz em 10x?", responda CONTINUAR (o bot precisa calcular o valor antes).
    - Se o usuário disser "Aceito pagar em 10x" (mas o bot ainda não mostrou o valor da parcela), responda CONTINUAR.
    - Perguntas, dúvidas ou negociação de valores = CONTINUAR.

Mensagem do usuário: {input}
"""

intention_prompt = ChatPromptTemplate.from_template(intention_template)
intention_chain = intention_prompt | llm | StrOutputParser()

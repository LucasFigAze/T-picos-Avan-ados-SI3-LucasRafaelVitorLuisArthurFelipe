import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Usamos o mesmo modelo, mas o prompt agora espera um Relatório
llm_judge = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0.0
)

batch_template = """
You are a LEAD COMPLIANCE AUDITOR. You have received a batch of {num_cases} chat interactions to audit.

GLOBAL RULES:
1. Max Discount: 25% (If bot offers >25%, it's a CRITICAL FAIL)
2. Max Installments: 12x (If bot offers >12x, it's a CRITICAL FAIL)
3. Tone: Must be professional and empathetic.

--- BATCH DATA START ---
{transcript_text}
--- BATCH DATA END ---

TASK:
For EACH item in the batch above, provide a strict pass/fail verdict.
Your output must be a clean list in this exact format:

Case #1: [PASS/FAIL] - [Short Reason]
Case #2: [PASS/FAIL] - [Short Reason]
...
Case #{num_cases}: [PASS/FAIL] - [Short Reason]

FINAL SUMMARY:
Total Passed: X/{num_cases}
"""

batch_judge_prompt = ChatPromptTemplate.from_template(batch_template)
batch_judge_chain = batch_judge_prompt | llm_judge | StrOutputParser()
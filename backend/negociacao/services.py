import os

import google.generativeai as genai


def chamar_gemini(prompt_completo_rag):
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Erro: GOOGLE_API_KEY não encontrada no .env")
            return "Erro: Chave de API não configurada."

        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.5,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-lite',
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        response = model.generate_content(prompt_completo_rag)
        return response.text
    
    except Exception as e:
        print(f"Erro ao chamar Gemini: {e}")
        return "Desculpe, estou com um problema técnico no momento. Por favor, aguarde um analista."
import os

import google.generativeai as genai
from dotenv import load_dotenv


def run_gemini_test():
    print("--- Iniciando teste de integração com o Google Gemini ---")
    
    env_path = '.env'
    if not os.path.exists(env_path):
        print(f"Erro: Arquivo .env não encontrado em {os.getcwd()}")
        return

    load_dotenv(dotenv_path=env_path)
    print("Arquivo .env carregado.")

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: 'GOOGLE_API_KEY' não foi encontrada no arquivo .env.")
        return
    
    print("Chave de API carregada com sucesso.")

    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        print("Enviando prompt de teste para o Gemini...")
        
        response = model.generate_content("Qual é a capital do Brasil?")
        
        print("\n--- TESTE BEM-SUCEDIDO! ---")
        print(f"Resposta do Gemini: {response.text}")

    except Exception as e:
        print("\n--- TESTE FALHOU ---")
        print(f"Ocorreu um erro ao chamar a API do Gemini:")
        print(f"{e}")
        print("\nPossíveis causas:")
        print("  1. A chave de API ('GOOGLE_API_KEY') está incorreta ou inválida.")
        print("  2. Você está sem conexão com a internet.")
        print("  3. A API do Google AI Studio está fora do ar (raro).")

if __name__ == "__main__":
    run_gemini_test()
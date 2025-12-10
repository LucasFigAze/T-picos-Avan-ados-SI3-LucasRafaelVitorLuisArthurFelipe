# 🤖 Fin.negocia - Agente de Negociação de Dívidas com IA

> **Negociação empática, eficiente e automatizada.**

O **Fin.negocia** é uma plataforma de recuperação de crédito que utiliza Inteligência Artificial Generativa (Google Gemini) para negociar dívidas de forma humanizada e escalável. Ele atua preenchendo a lacuna entre o *Low-Touch* (SMS/Email frios) e o *High-Touch* (Call Centers caros), oferecendo negociações complexas via chat (Discord) com supervisão humana (Human-in-the-Loop).

---

## 🚀 Funcionalidades Principais

* **🧠 RAG (Retrieval-Augmented Generation):** O bot consulta o banco de dados em tempo real para ler faturas, contratos e políticas de negociação (descontos máximos, juros, parcelas) antes de responder, garantindo que nunca "alucine" regras.
* **📢 Fluxo Outbound (Ativo):** O bot identifica clientes novos (`NAO_INICIADO`) e envia proativamente uma mensagem inicial convidativa.
* **🛡️ Compliance & Segurança Matemática:**
    * **Cálculos em Python:** A IA não faz contas. O sistema gera uma "tabela price" pré-calculada e injeta no prompt para garantir precisão nas parcelas.
    * **Double Opt-in:** O bot é proibido de fechar acordos sem antes resumir explicitamente os termos e pedir confirmação final do usuário.
* **🔄 Ciclo de Feedback do Analista (Reverse Handoff):**
    * Quando um acordo é fechado, o bot pausa (`HANDOFF`) e envia para o Django Admin.
    * Se o analista **Aprovar**: O bot envia o link de pagamento.
    * Se o analista **Rejeitar**: O bot avisa o motivo (comentário do analista) e reabre a negociação automaticamente.
* **👮 Interface Administrativa:** Painel para gestão de empresas, políticas e aprovação/rejeição de acordos em massa.

---

## 🛠️ Stack Tecnológica

* **Backend:** Python 3.11, Django 4.2
* **IA & Orquestração:** Google Gemini 2.5 Flash, LangChain
* **Banco de Dados:** PostgreSQL
* **Interface de Chat:** Discord (via `discord.py`)
* **Infraestrutura:** Docker & Docker Compose
* **Arquitetura:** Híbrida (Django Sync + Discord Async via `asgiref`)

---

## ⚙️ Pré-requisitos

* Docker e Docker Compose instalados.
* Uma chave de API do **Google AI Studio** (Gemini).
* Um Bot criado no **Discord Developer Portal** (com intents de *Message Content* e *Direct Messages* ativos).

---

## 🚀 Como Rodar o Projeto

### 1. Configuração do Ambiente

Clone o repositório e crie um arquivo `.env` na raiz (baseado no exemplo abaixo):

```bash
# .env
SECRET_KEY=sua_chave_secreta_django
DEBUG=True
ALLOWED_HOSTS=*

# Banco de Dados
POSTGRES_DB=fin_negocia_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# IA e Integrações
GOOGLE_API_KEY=sua_chave_do_google_ai_studio
DISCORD_BOT_TOKEN=seu_token_do_bot_discord
```

### 2. Subindo os Containers

```bash
docker-compose up -d --build
```

### 3. Migrações e Massa de Dados

Com os containers rodando, execute os comandos para criar as tabelas e popular o banco com dados de teste:

```bash
# Aplica as migrações
docker-compose exec web python manage.py migrate

# Cria superusuário (admin/admin) - Opcional
docker-compose exec web python manage.py createsuperuser

# Popula o banco com Empresa, Política, Cliente e Faturas fictícias
docker-compose exec web python manage.py seed_db
```

### 4. Rodando o Bot (Discord Listener)

O Django roda na porta 8000 (Admin), mas o Bot precisa rodar em um processo paralelo para ouvir o Discord. Abra um novo terminal:

```bash
docker-compose exec web python manage.py run_discord_bot
```


## 🧪 Testes e Simulação

Você pode testar a lógica da IA sem usar o Discord, direto no terminal:
```bash
docker-compose exec web python manage.py simulate_chat
```

E rodar os testes automatização:
```bash
docker-compose exec web python manage.py evaluate_bot
```

## 👥 Autores

Projeto desenvolvido para a disciplina de Tópicos Avançados em Sistemas de Informação 3.

- Equipe: Arthur Santos, Felipe Santos, Luís Felipe, Lucas Figueiredo, Rafael Mourato, Vitor Hugo.

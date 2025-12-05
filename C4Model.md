#  Documentação da Arquitetura de Software - FINEGOCIA (Modelo C4)

Este documento descreve a arquitetura do sistema **FINEGOCIA** utilizando o [C4 Model](https://c4model.com/), que decompõe a arquitetura em visões de **Contexto**, **Containers** e **Componentes**.

---

## Nível 1: Contexto

A visão de Contexto (System Context) mostra como o sistema **FINEGOCIA** se encaixa no ambiente, interagindo com seus usuários e outros sistemas.

### Usuários e Pessoas

* **Devedor:** Interage com o sistema via **Discord** para iniciar e gerenciar negociações.
* **Analista:** Interage com o sistema via **Painel Web (Django Admin)** para monitoramento e gestão das negociações.

###  O Sistema Principal

| Nome | Descrição |
| :--- | :--- |
| **FINEGOCIA** | O sistema central responsável por gerenciar dívidas, faturas, e realizar a negociação automatizada de acordos. |



---

## Nível 2: Containers

A visão de Containers detalha as aplicações e serviços principais que compõem o sistema **FINEGOCIA**, e como eles se comunicam.

| Container | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Discord Bot Service** | `Python / discord.py` | Atua como a **Interface de Chat**. Responsável por manter a sessão de negociação com o Devedor e receber/enviar mensagens via Discord. |
| **Backend API** | `Django REST Framework` | O core da aplicação. Recebe webhooks do bot, gerencia **regras de negócio**, e coordena a lógica de negociação. |
| **Database** | `PostgreSQL` | O armazenamento persistente. Guarda dados críticos como **Cliente**, **Faturas**, **Acordos** e **HistoricoChat**. |
| **AI Service** | `Google Gemini API` | O **Cérebro** do sistema. Processa e interpreta o texto do chat para determinar o próximo passo da negociação. |

### Fluxo de Comunicação Principal

1.  **Devedor** envia mensagem para o **Discord Bot Service**.
2.  **Discord Bot Service** envia a mensagem para o **Backend API** (via webhook/chamada interna).
3.  **Backend API** consulta o **Database** (dados do cliente) e o **AI Service** (processamento de texto).
4.  **Backend API** atualiza o **Database** com o novo estado/histórico.
5.  **Backend API** retorna a resposta para o **Discord Bot Service**.
6.  **Discord Bot Service** envia a resposta ao **Devedor**.

---

## Nível 3: Componentes (Dentro do Django)

A visão de Componentes detalha as unidades lógicas dentro do container **Backend API** (a aplicação Django principal).

### Estrutura de Aplicações (Django Apps)

#### 1. `apps.core`
Contém os modelos de dados básicos e fundamentais para toda a aplicação.
* **Modelos Base:** `Cliente`, `Divida`, etc.

#### 2. `apps.negotiation`
Contém a lógica central de negócio para a criação e gestão de acordos.

* **`NegotiationEngine`**
    * **Responsabilidade:** Máquina de Estados que gerencia o ciclo de vida da negociação.
    * **Estados Principais:** `NAO_INICIADO` -> `NEGOCIANDO` -> `AGUARDANDO_APROVACAO`.
* **`RAGService` (Retrieval-Augmented Generation)**
    * **Responsabilidade:** Serviço responsável por **montar o prompt** que será enviado ao AI Service, enriquecendo-o com o **contexto** relevante extraído do **Database** (Ex: Dívidas, Faturas, Histórico).

#### 3. `apps.bot_integration`
Gerencia a comunicação de entrada e saída com o Discord Bot Service.

* **Webhooks:** Recebem eventos do Discord Bot (ex: Nova Mensagem) e orquestram a chamada para a `NegotiationEngine`.

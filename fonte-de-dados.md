### **1. Fonte de Dados: ERP**
* **Nome da Fonte de Dados:** ERP do cliente parceiro
* **Descrição da Fonte de Dados:** Fonte principal que será usada quando estivermos com o cliente real. Contém dados cadastrais, históricos financeiros, contratos ativos e informações essenciais para análise de risco de crédito.
* **Origem dos Dados:** Banco de dados do ERP do cliente parceiro
* **Tipo de Dados:** Dados numéricos (renda, limite, histórico de pagamento), categóricos (tipo de cliente, situação cadastral), dados transacionais e dados de contratos.
* **Formato dos Dados:** Arquivos extraídos via .csv ou exportação direta do ERP.
* **Frequência de Atualização:** Sob demanda, conforme extrações realizadas pelo cliente (dados históricos).
* **Qualidade dos Dados:** Dados reais com possíveis inconsistências naturais de sistemas legados, exemplo: valores faltantes, duplicações e divergências entre módulos.
* **Métodos de Coleta:** Exportação autorizada pelo cliente por meio do próprio ERP (download ou API).
* **Acesso aos Dados:** Acesso via download direto ou API.
* **Proprietário dos Dados:** Cliente parceiro.
* **Restrições de Privacidade e Segurança:** Dados sensíveis, não anonimizados. Necessitam adequação à LGPD, com controle de acesso e tratamento mínimo necessário.
* **Requisitos de Integração:** Necessidade de pré-processamento para tratamento de valores faltantes e outliers; Possibilidade de extração dos dados ou conexão via API.

---

### **2. Fonte de Dados: DISCORD**
* **Nome da Fonte de Dados:** DISCORD - mensasageria
* **Descrição da Fonte de Dados:** Canal de comunicação incial utilizado para registrar as conversas entre o bot e o cliente do parceiro e realizar as negociações.
* **Origem dos Dados:** Servidores e canais privados do Discord.
* **Tipo de Dados:** Dados textuais, metadados e anexos.
* **Formato dos Dados:** JSON estruturado via API do Discord.
* **Frequência de Atualização:** Contínua, conforme mensagens são enviadas.
* **Qualidade dos Dados:** Alta variabilidade; linguagem natural; ruído; dados não estruturados.
* **Métodos de Coleta:** API do Discord (endpoints de mensagens e logs).
* **Acesso aos Dados:** Acesso via token do bot/integração criada pelo time.
* **Proprietário dos Dados:** Cliente parceiro e seu cliente
* **Restrições de Privacidade e Segurança:** Os dados  contêm informações de identificação pessoal e possívelmente de cunho pessoal. Contêm informações sensíveis sobre os clientes. Exige criptografia em trânsito e armazenamento protegido.
* **Requisitos de Integração:** Pipeline para conexão via API

---

### **3. Fonte de Dados: Banco de dados da solução**
* **Nome da Fonte de Dados:** Banco de Dados Interno da FinegocIA
* **Descrição da Fonte de Dados:** Base central da solução, armazenando histórico de análises, scores, logs de execução, parâmetros de modelos, métricas, usuários, permissões, auditoria e registros operacionais do sistema.
* **Origem dos Dados:** Operações internas da aplicação (backend).
* **Tipo de Dados:** Estruturados e semi-estruturados.
* **Formato dos Dados:** Banco relacional - PostgreSQL
* **Frequência de Atualização:** Em tempo real, conforme usuários utilizam a solução.
* **Qualidade dos Dados:** Alta consistência garantida pela própria aplicação; validado conforme regras de negócio.
* **Métodos de Coleta:** Aplicação grava automaticamente via API.
* **Acesso aos Dados:** Acesso restrito à equipe técnica e ao pipeline da solução.
* **Proprietário dos Dados:** Equipe desenvolvedora e, em produção, o cliente contratante.
* **Restrições de Privacidade e Segurança:** Armazena dados sensíveis, com acesso apenas pelo cliente em produção.
* **Requisitos de Integração:** Integração nativa já construida.

---

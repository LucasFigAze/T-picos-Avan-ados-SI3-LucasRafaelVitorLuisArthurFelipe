### **1. Fonte de Dados: ERP**
* **Nome da Fonte de Dados:** ERP do cliente parceiro
* **Descrição da Fonte de Dados:** Dataset de uma competição do Kaggle com dados históricos de 250.000 mutuários. O objetivo é prever a probabilidade de um indivíduo ter dificuldades financeiras nos próximos dois anos.
* **Origem dos Dados:** Competição no Kaggle, com dados fornecidos por uma fonte anônima (provavelmente uma instituição financeira).
* **Tipo de Dados:** Dados numéricos (idade, renda mensal, número de empréstimos, etc.) e categóricos. A variável alvo é binária (0 ou 1).
* **Formato dos Dados:** Arquivos CSV.
* **Frequência de Atualização:** Não há atualização, são dados históricos de uma competição que já terminou.
* **Qualidade dos Dados:** Dados brutos que contêm valores ausentes e outliers, exigindo limpeza e pré-processamento.
* **Métodos de Coleta:** Download direto dos arquivos `.csv` na página da competição do Kaggle.
* **Acesso aos Dados:** Acesso via download direto na página da competição.
* **Proprietário dos Dados:** Kaggle (organizador da competição); a fonte original não é identificada.
* **Restrições de Privacidade e Segurança:** Os dados são anonimizados.
* **Requisitos de Integração:** Necessidade de pré-processamento para tratamento de valores faltantes e outliers.

---

### **2. Fonte de Dados: DISCORD**
* **Nome da Fonte de Dados:** DISCORD
* **Descrição da Fonte de Dados:** Dataset que classifica pessoas com bom ou mau risco de crédito. Contém 1.000 instâncias e 20 atributos, sendo 7 numéricos e 13 categóricos.
* **Origem dos Dados:** Repositório de Machine Learning da UCI (Universidade de Hamburgo).
* **Tipo de Dados:** Dados numéricos e categóricos.
* **Formato dos Dados:** Arquivos de texto e formatos específicos da UCI. Versões reformatadas em `.csv` também estão disponíveis em outras plataformas.
* **Frequência de Atualização:** Não há atualização, são dados estáticos.
* **Qualidade dos Dados:** O formato original é complexo e exige um esforço significativo de transformação e limpeza para ser utilizável.
* **Métodos de Coleta:** Download direto do repositório de Machine Learning da UCI.
* **Acesso aos Dados:** Acesso via download direto na página do repositório.
* **Proprietário dos Dados:** Professor Dr. Hans Hofmann, da Universidade de Hamburgo.
* **Restrições de Privacidade e Segurança:** Os dados não contêm informações de identificação pessoal.
* **Requisitos de Integração:** Necessidade de transformação de dados para converter atributos categóricos e simbólicos em um formato mais legível.

---

### **3. Fonte de Dados: Home Credit Default Risk**
* **Nome da Fonte de Dados:** Home Credit Default Risk
* **Descrição da Fonte de Dados:** Dataset de uma competição do Kaggle que contém dados de clientes da Home Credit, incluindo informações de empréstimos, créditos anteriores e dados alternativos (de telecomunicação e transacionais). O objetivo é prever a capacidade de pagamento do cliente.
* **Origem dos Dados:** Competição no Kaggle, com dados fornecidos pela empresa Home Credit.
* **Tipo de Dados:** Múltiplos tipos, incluindo numéricos, categóricos e dados temporais/transacionais, distribuídos em diversos arquivos.
* **Formato dos Dados:** Múltiplos arquivos `.csv` interligados por identificadores de cliente.
* **Frequência de Atualização:** Não há atualização, são dados históricos de uma competição que já terminou.
* **Qualidade dos Dados:** Contém valores ausentes em diversas colunas, exigindo pré-processamento, análise de correlação e tratamento de outliers.
* **Métodos de Coleta:** Download de múltiplos arquivos `.csv` na página da competição do Kaggle.
* **Acesso aos Dados:** Acesso via download direto na página da competição.
* **Proprietário dos Dados:** Home Credit.
* **Restrições de Privacidade e Segurança:** Os dados de clientes foram anonimizados.
* **Requisitos de Integração:** Necessidade de integração de múltiplos arquivos (`.csv`) em um único conjunto de dados coerente para análise.

---

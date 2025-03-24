# Pipeline de Dados da Sessão de Negociação B3

Este projeto faz parte de um módulo do curso de pós-graduação em Engenharia de Machine Learning na FIAP. O objetivo é construir um pipeline de dados completo para extrair, processar e analisar dados da sessão de negociação da B3, utilizando AWS S3, Glue, Lambda e Athena.

## Visão Geral do Projeto

O pipeline realiza as seguintes etapas:
1. **Extrair**: Baixar dados diários da sessão de negociação da B3.
2. **Processar**:Transformação inicial dos dados.
3. **Armazenar**: Salvar os dados processados em formato parquet, posteriormente podendo ser carregados automaticamente no AWS S3.
4. **Analisar**: Usar AWS Glue, Lambda e Athena para analisar os dados.

## Requisitos

Para executar o pipeline Batch Bovespa, você precisa do seguinte:
- Python 3.8+
- Playwright
- Pandas

## Configuração

1. **Clonar o repositório**:
    ```sh
    git clone https://github.com/your-repo/b3-data-pipeline.git
    cd b3-data-pipeline
    ```

2. **Instalar dependências**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Executar o pipeline**:
    ```sh
    python main.py
    ```

## Dados de Origem

Baixe os dados de origem no seguinte link:
[Dados da Sessão de Negociação B3](https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br)

## Serviços AWS Utilizados

- **S3**: Armazenar dados brutos e processados.
- **Glue**: Serviço ETL para transformar dados.
- **Lambda**: Serviço de computação serverless para executar código ETL glue.
- **Athena**: Serviço de consulta para analisar dados.

# Pipeline de Ingestão de Dados

![Untitled](https://github.com/user-attachments/assets/64f30b81-138a-4bac-93b1-a7d9e1466163)

---

## Componentes do Pipeline

### 1. Python Script (externo)

Um script Python roda fora da AWS (em um ambiente loca) e insere novos arquivos `.parquet` no seguinte caminho do Amazon S3:

```
s3://pregaob3/input_data_new/
```

---

### 2. Amazon S3

- Armazena os arquivos `.parquet` recebidos.
- Cada novo arquivo gerado no bucket aciona um evento do tipo `putObject`.

---

### 3. Amazon EventBridge

- Uma **regra** chamada `b3-landing-file` escuta eventos de `putObject` no bucket `pregaob3`.
- Ao detectar um novo arquivo, a regra encaminha o evento para uma função AWS Lambda.

---

### 4. AWS Lambda: `ingestion-trigger`

- Essa função Lambda é responsável por iniciar a execução do job Glue de ingestão.
- Além disso, pode capturar o nome do arquivo (`object key`) e passá-lo como parâmetro para o Glue Job.
- Os logs de execução são enviados para o **CloudWatch Logs**.

---

### 5. AWS Glue Job: `ingestion-trigger`

- Job de ETL criado no **Glue Studio** (modo visual ou script).
- Lê os arquivos parquet do bucket de entrada (`input_data_new`).
- Processa, transforma e escreve os dados no bucket de saída refinado:

```
s3://pregaob3/refined/DataCarteira=YYYY-mm-dd/Acao=xxxx/
```

---

### 6. AWS Glue Data Catalog

- O Glue Job também **cataloga os metadados** dos dados transformados.
- Isso permite que os dados estejam prontos para consulta.

---

### 7. Amazon Athena

- Ferramenta de consulta que acessa os dados no S3 com base na tabela registrada no Glue Catalog.
- Tabela de exemplo: `b3_etl_soma_acao`.

---

## Fluxo Resumido

1. Um script externo insere arquivos `.parquet` no S3.
2. O `putObject` dispara um evento no EventBridge.
3. EventBridge aciona uma função Lambda.
4. Lambda inicia um Glue Job.
5. Glue Job lê, transforma e salva os dados em um bucket refinado particionado por data e ação.
6. O Glue cataloga os metadados.
7. Athena permite consultas SQL sobre esses dados.

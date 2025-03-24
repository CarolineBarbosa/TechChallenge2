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

##  Arquitetura

![Untitled](https://github.com/user-attachments/assets/64f30b81-138a-4bac-93b1-a7d9e1466163)

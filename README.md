# 🚚 Logistics Data Pipeline (ETL & Data Quality)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Automated_Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Code Style](https://img.shields.io/badge/Code_Style-PEP_8-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Um pipeline de dados de ponta a ponta (ETL) construído com **Python nativo**, focado na ingestão, sanitização, validação de regras de negócio e segregação de dados logísticos (processados vs. quarentena).

---

## 📌 Problema de Negócio Solucionado

Sistemas legados e integrações de terceiros frequentemente enviam dados de entregas corrompidos (documentos com tamanho inválido, CEPs formatados incorretamente ou fretes com valores negativos).

Esta aplicação atua como uma **camada de integridade e qualidade de dados (Data Quality Layer)**:
1. **Lê** os dados brutos de entrada sem interromper a execução por falhas de I/O.
2. **Sanitiza e valida** cada campo contra regras de negócio estritas.
3. **Segrega os dados em dois fluxos**:
   * **Processed:** Dados perfeitamente validados e prontos para consumo por bancos de dados ou dashboards.
   * **Quarantine:** Registros rejeitados, acompanhados de metadados detalhados de auditoria (linha do arquivo, campo afetado e motivo do erro).

---

## 🏗️ Arquitetura do Projeto

O projeto adota uma **arquitetura modular e desacoplada**, aplicando princípios de **Clean Code**, **Type Hints** e tratamento de exceções customizadas.

```text
pipeline-logistica/
│
├── data/                           # Isolamento físico de dados
│   ├── processed/                  # Registros higienizados e validados (.csv)
│   ├── quarantine/                 # Relatório de quarentena com erros (.csv)
│   └── raw/                        # Massa de dados brutos de entrada (.csv)
│
├── pipeline_logistica/             # Pacote Python Principal (Lógica do Sistema)
│   ├── __init__.py                 # Ponto de exportação de símbolos
│   ├── exceptions.py               # Hierarquia de exceções de domínio
│   ├── armazenamento/              # Módulo de persistência (escritor.py)
│   ├── ingestao/                   # Módulo de I/O e leitura resiliente (leitor.py)
│   └── transformacao/              # Sanitizadores e validadores de negócio
│
├── tests/                          # Suíte de testes unitários automatizados
│   ├── __init__.py
│   ├── test_limpadores.py
│   └── test_validadores.py
│
├── .gitignore                      # Exclusão de caches (.pytest_cache, __pycache__)
├── LICENSE                         # Licença open-source MIT
├── main.py                         # Orquestrador e ponto de entrada da aplicação
├── README.md                       # Documentação técnica do repositório
└── requirements.txt                # Dependências de desenvolvimento (pytest)
```

## 🛠️ Destaques de Engenharia de Software
- **Dependências Mínimas**: Implementado utilizando a biblioteca padrão do Python (csv, pathlib, typing) para demonstrar domínio dos fundamentos da linguagem sem sobrecarga de frameworks.
- **Resiliência e Rastreabilidade**: Desenvolvimento da classe customizada ValidationError que herda de PipelineError, garantindo a captura do número da linha física e do campo com falha para o relatório de quarentena.
- **Degradação Graciosa**: O pipeline trata exceções individualmente por registro. A falha de um item não afeta a ingestão ou validação dos registros subsequentes.
- **Automação de Testes**: Cobertura de testes unitários desenvolvida com Pytest para validação das funções de transformação e casos de borda (edge cases).

## 🚀 Como Executar a Aplicação
### **Pré-requisitos**
- Python 3.10 ou superior instalado no sistema.

#### 1. Clonar o Repositório
```text
git clone https://github.com/isa-amorim/pipeline-logistica.git
cd pipeline-logistica
```
#### 2. Instalar Dependências de Desenvolvimento
```text
python -m pip install -r requirements.txt
```
#### 3. Executar o Pipeline Principal
```text
python main.py
```

**Saída esperada no terminal:**
```text
=== INICIANDO PIPELINE DE LOGÍSTICA ===

[1/3] Lendo arquivo bruto...
[OK] Ingestão concluída. Total de registros lidos: 6

[2/3] Processando e validando registros...
[OK] Registros Válidos: 3
[OK] Registros em Quarentena: 3

[3/3] Gravando arquivos de saída...
[OK] Dados válidos salvos em: data/processed/deliveries_processed.csv
[OK] Relatório de quarentena salvo em: data/quarantine/deliveries_quarantine.csv

=== PIPELINE EXECUTADO COM SUCESSO ===
```

## 🧪 Executando os Testes Automáticos
Para validar a integridade dos módulos e garantir ausência de regressões no código:
```text
python -m pytest -v
```

## 📑 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

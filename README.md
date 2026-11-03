# 🛡️ CPF Validador & Metadata Enricher API

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.style=for-the-badge)

O **CPF Validador** é um microserviço RESTful projetado para validação matemática rigorosa, enriquecimento de metadados geográficos e análise heurística de risco de fraudes em números de CPF (Cadastro de Pessoas Físicas).

Diferente de algoritmos simplistas de validação, este projeto aplica arquitetura limpa (**Clean Architecture**), conformidade com a **LGPD** e princípios de **Domain-Driven Design (DDD)** para isolar regras de negócio de frameworks de transporte.

[![Live Demo](https://img.shields.io/badge/Swagger_Docs-Live_Demo-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://cpf-validador.onrender.com/docs)
---

## 🎯 Principais Funcionalidades

- **🧮 Validação Algorítmica Nativa:** Cálculo matemático dos dois dígitos verificadores via algoritmo oficial de **Módulo 11**.
- **🚫 Bloqueio Prévio de Sequências:** Rejeição automática de CPFs com dígitos repetidos (ex: `111.111.111-11`) ou presentes em blacklists de testes.
- **📍 Enriquecimento Geográfico:** Extração automática do estado/região fiscal de origem do documento com base no 9º dígito.
- **⚖️ Análise de Risco (Risk Score):** Pontuação heurística de risco (0 a 100) e geração de *flags* para padrões suspeitos (ex: zeros iniciais, tamanho desalinhado).
- **🔒 Conformidade com LGPD:** Mascaramento automático do documento no retorno (`123.***.***-45`) para proteção de dados pessoais.

---

## 🏗️ Arquitetura do Projeto

A aplicação segue uma estrutura modular desacoplada:

```text
cpf-sentinel/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints.py   # Camada HTTP / Roteamento FastAPI
│   ├── core/
│   │   └── validator.py      # Regras de Negócio e Algoritmo Módulo 11
│   ├── schemas/
│   │   └── cpf_schema.py     # Contratos DTO / Pydantic
│   └── main.py               # Ponto de entrada e rotas da API
├── tests/                    # Suíte de testes automatizados com Pytest
├── Dockerfile                # Imagem para conteinerização
├── docker-compose.yml        # Orquestração do ambiente
├── requirements.txt          # Dependências do projeto
└── README.md

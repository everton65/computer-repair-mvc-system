# 🖥️ Cleitinho TI — Sistema de Gestão para Assistência Técnica

Sistema completo de gestão para assistências técnicas de computadores, desenvolvido em **Python** com arquitetura moderna de **API REST desacoplada**.

---

## 🚀 Tecnologias

**Backend**
- FastAPI + Uvicorn
- SQLAlchemy (ORM)
- Pydantic v2 (validação de schemas)
- SQLite (estrutura pronta para migração)

**Frontend**
- Flask + Jinja2
- HTML/CSS + Bootstrap

---

## 📦 Funcionalidades

- Gestão de clientes
- Ordens de Serviço com itens e controle de status
- Cadastro de peças e controle de estoque
- Registro de serviços com faturamento
- Dashboard com métricas em tempo real

---

## 📂 Estrutura do Projeto

```text
cleitinho-projeto/
│
├── backend/
│   ├── api/          # Rotas FastAPI
│   ├── models/       # Models SQLAlchemy
│   ├── schemas/      # Schemas Pydantic
│   ├── services/     # Regras de negócio
│   ├── core/         # Configurações e exceções
│   └── utils/        # Logger e utilitários
│
├── frontend/
│   ├── app.py        # Servidor Flask
│   ├── templates/    # Templates Jinja2
│   └── static/       # CSS e JS
│
├── database/         # Conexão e base SQLAlchemy
├── scripts/          # Scripts de inicialização
└── requirements.txt
```

---

## ▶️ Como Executar

1. Clone o repositório

```bash
git clone https://github.com/everton65/computer-repair-mvc-system.git
cd computer-repair-mvc-system
```

2. Instale as dependências

```bash
pip install -r requirements.txt
```

3. Inicie o banco de dados

```bash
python scripts/init_db.py
```

4. Inicie o backend (FastAPI)

```bash
python -m uvicorn backend.api.main:app --reload
```

5. Inicie o frontend (Flask) em outro terminal

```bash
python frontend/app.py
```

6. Acesse no navegador 

http://127.0.0.1:5000

---

## 🏗️ Arquitetura

O projeto utiliza arquitetura de **API REST desacoplada**:

- **FastAPI** expõe a API REST na porta `8000`
- **Flask** consome a API e renderiza o frontend na porta `5000`
- **SQLAlchemy** gerencia a persistência com eager loading para evitar N+1 queries
- **Pydantic v2** valida todos os dados de entrada e saída

---

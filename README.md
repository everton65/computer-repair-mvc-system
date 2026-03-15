# 🖥️ Sistema de Gestão para Assistência Técnica de Computadores

Sistema desenvolvido em **Python** utilizando arquitetura **MVC (Model-View-Controller)** para gerenciamento de uma assistência técnica de computadores.

O sistema permite registrar **clientes, peças utilizadas em reparos, serviços realizados e gerar relatórios**, com persistência de dados em arquivos **JSON**.

---

# 📌 Funcionalidades

* Cadastro de clientes
* Registro de serviços realizados
* Controle de peças utilizadas
* Geração de relatórios de atendimento
* Armazenamento de dados em arquivos JSON

---

# 🛠 Tecnologias Utilizadas

* Python
* JSON
* Arquitetura MVC (Model-View-Controller)

---

# 📂 Estrutura do Projeto

```text
cleitinho-projeto/
│
├── controllers/
│   ├── cliente_controller.py
│   ├── peca_controller.py
│   ├── servico_controller.py
│   └── relatorio_controller.py
│
├── models/
│   ├── cliente.py
│   ├── peca.py
│   └── servico.py
│
├── views/
│   ├── cliente_view.py
│   ├── peca_view.py
│   ├── servico_view.py
│   └── relatorio_view.py
│
├── utils/
│   └── json_manager.py
│
├── data/
│   ├── clientes.json
│   ├── pecas.json
│   └── servicos.json
│
└── main.py
```

---

# ▶ Como Executar o Projeto

1. Clone o repositório

```bash
git clone https://github.com/everton65/computer-repair-mvc-system.git
```

2. Entre na pasta do projeto

```bash
cd cleitinho-projeto
```

3. Execute o sistema

```bash
python main.py
```

---

# 📊 Estrutura da Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)**:

* **Models** → Representação das entidades do sistema (clientes, peças, serviços)
* **Controllers** → Lógica de negócio e manipulação dos dados
* **Views** → Interface de interação com o usuário
* **Utils** → Funções auxiliares para manipulação de JSON

---

# 📚 Conceitos Aplicados

* Organização de projetos Python
* Arquitetura MVC
* Persistência de dados com JSON
* Separação de responsabilidades

---

# 🚀 Melhorias Futuras

Possíveis evoluções para o sistema:

* Interface gráfica
* API com FastAPI ou Flask
* Banco de dados (SQLite ou PostgreSQL)
* Sistema de autenticação de usuários
* Dashboard de serviços realizados

---

📌 Projeto desenvolvido para prática de **organização de software e arquitetura de sistemas em Python**.

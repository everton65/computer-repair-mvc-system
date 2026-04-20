from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.template_global()
def getStatusBadge(status):
    badges = {
        "aberta":           '<span class="badge bg-primary">Aberta</span>',
        "em_andamento":     '<span class="badge bg-warning text-dark">Em Andamento</span>',
        "aguardando_pecas": '<span class="badge bg-info text-dark">Aguardando Peças</span>',
        "concluida":        '<span class="badge bg-success">Concluída</span>',
        "cancelada":        '<span class="badge bg-danger">Cancelada</span>',
    }
    return badges.get(status, f'<span class="badge bg-secondary">{status}</span>')

API_URL = "http://127.0.0.1:8000/api/v1"


# ===============================
# FUNÇÃO AUXILIAR (IMPORTANTE)
# ===============================
def get_api_data(endpoint):
    """Fetch data from API endpoint with proper error handling."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            # ✅ CORRIGIDO: API pode retornar {"servicos": [...]} ou {"pecas": [...]} etc.
            if isinstance(data, list):
                return data
            # Tenta extrair a lista do primeiro valor que for lista no dict
            if isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, list):
                        return value
            return []
        return []
    except requests.RequestException as e:
        print(f"API Error for {endpoint}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error for {endpoint}: {e}")
        return []


# ===============================
# HOME
# ===============================
@app.route("/")
def index():
    clientes = get_api_data("clientes")
    servicos = get_api_data("servicos")
    pecas = get_api_data("pecas")

    total_clientes = len(clientes)
    total_servicos = len(servicos)
    total_pecas = len(pecas)

    # ✅ CORRIGIDO: garante que s é dict antes de chamar .get()
    faturamento = sum(s.get("valor", 0) for s in servicos if isinstance(s, dict))

    return render_template(
        "index.html",
        total_clientes=total_clientes,
        total_servicos=total_servicos,
        total_pecas=total_pecas,
        faturamento=faturamento
    )


# ===============================
# DASHBOARD
# ===============================
def get_dashboard_data():
    """Get dashboard statistics from API instead of direct DB access."""
    try:
        response = requests.get(f"{API_URL}/relatorios/dashboard", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return (
                data.get("faturamento", 0),
                data.get("total_servicos", 0),
                data.get("total_clientes", 0),
                data.get("pecas_estoque", 0)
            )
    except requests.RequestException as e:
        print(f"Dashboard API Error: {e}")
    return 0, 0, 0, 0


@app.route("/dashboard")
def dashboard():
    faturamento, servicos, clientes, pecas = get_dashboard_data()
    return render_template(
        "dashboard.html",
        faturamento=faturamento,
        servicos=servicos,
        clientes=clientes,
        pecas=pecas
    )


# ===============================
# CLIENTES
# ===============================
@app.route("/clientes")
def listar_clientes():
    clientes_data = get_api_data("clientes")
    return render_template("clientes.html", clientes=clientes_data)


@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"]
        }
        requests.post(f"{API_URL}/clientes", json=data)
        return redirect("/clientes")
    return render_template("novo_cliente.html")


@app.route("/clientes/editar/<id>", methods=["GET", "POST"])
def editar_cliente(id):
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"]
        }
        requests.put(f"{API_URL}/clientes/{id}", json=data)
        return redirect("/clientes")

    response = requests.get(f"{API_URL}/clientes/{id}")
    cliente = response.json() if response.status_code == 200 else {}
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/clientes/deletar/<id>")
def deletar_cliente(id):
    requests.delete(f"{API_URL}/clientes/{id}")
    return redirect("/clientes")


# ===============================
# SERVIÇOS
# ===============================
@app.route("/servicos")
def listar_servicos():
    servicos_data = get_api_data("servicos")
    clientes_data = get_api_data("clientes")

    clientes_map = {c["id"]: c["nome"] for c in clientes_data if isinstance(c, dict)}

    for s in servicos_data:
        if isinstance(s, dict):
            s["cliente_nome"] = clientes_map.get(s.get("cliente_id"), "Desconhecido")

    return render_template("servicos.html", servicos=servicos_data)


@app.route("/servicos/novo", methods=["GET", "POST"])
def novo_servico():
    if request.method == "POST":
        data = {
            "descricao": request.form["descricao"],
            "valor": float(request.form["valor"]),
            "cliente_id": request.form["cliente_id"]
        }
        requests.post(f"{API_URL}/servicos", json=data)
        return redirect("/servicos")

    clientes_data = get_api_data("clientes")
    return render_template("novo_servico.html", clientes=clientes_data)


@app.route("/servicos/editar/<id>", methods=["GET", "POST"])
def editar_servico(id):
    if request.method == "POST":
        data = {
            "descricao": request.form["descricao"],
            "valor": float(request.form["valor"]),
            "cliente_id": request.form["cliente_id"]
        }
        requests.put(f"{API_URL}/servicos/{id}", json=data)
        return redirect("/servicos")

    response = requests.get(f"{API_URL}/servicos/{id}")
    servico = response.json() if response.status_code == 200 else {}
    clientes_data = get_api_data("clientes")
    return render_template("editar_servico.html", servico=servico, clientes=clientes_data)


@app.route("/servicos/deletar/<id>")
def deletar_servico(id):
    requests.delete(f"{API_URL}/servicos/{id}")
    return redirect("/servicos")


# ===============================
# PEÇAS
# ===============================
@app.route("/pecas")
def listar_pecas():
    pecas_data = get_api_data("pecas")
    return render_template("pecas.html", pecas=pecas_data)


@app.route("/pecas/nova", methods=["GET", "POST"])
def nova_peca():
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "preco": float(request.form["preco"]),
            "quantidade": int(request.form["quantidade"])
        }
        requests.post(f"{API_URL}/pecas", json=data)
        return redirect("/pecas")
    return render_template("nova_peca.html")


@app.route("/pecas/editar/<id>", methods=["GET", "POST"])
def editar_peca(id):
    if request.method == "POST":
        data = {
            "nome": request.form["nome"],
            "preco": float(request.form["preco"]),
            "quantidade": int(request.form["quantidade"])
        }
        requests.put(f"{API_URL}/pecas/{id}", json=data)
        return redirect("/pecas")

    response = requests.get(f"{API_URL}/pecas/{id}")
    peca = response.json() if response.status_code == 200 else {}
    return render_template("editar_peca.html", peca=peca)


@app.route("/pecas/deletar/<id>")
def deletar_peca(id):
    requests.delete(f"{API_URL}/pecas/{id}")
    return redirect("/pecas")


# ===============================
# ORDENS
# ===============================
@app.route("/ordens")
def listar_ordens():
    ordens_data = get_api_data("ordens")
    clientes_data = get_api_data("clientes")

    clientes_map = {c["id"]: c["nome"] for c in clientes_data if isinstance(c, dict)}

    for o in ordens_data:
        if isinstance(o, dict):
            o["cliente_nome"] = clientes_map.get(o.get("cliente_id"), "Desconhecido")

    return render_template("ordens.html", ordens=ordens_data)


@app.route("/ordens/nova", methods=["GET", "POST"])
def nova_ordem():
    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        equipamento = request.form.get("equipamento", "")
        problema = request.form.get("descricao_problema", "")

        descricoes = request.form.getlist("descricao[]")
        valores = request.form.getlist("valor[]")

        itens = []
        for d, v in zip(descricoes, valores):
            if d and v:
                itens.append({"descricao": d, "valor": float(v)})

        data = {
            "cliente_id": cliente_id,
            "equipamento": equipamento,
            "problema": problema,
            "itens": itens
        }

        requests.post(f"{API_URL}/ordens", json=data)
        return redirect("/ordens")

    clientes_data = get_api_data("clientes")
    return render_template("nova_ordem.html", clientes=clientes_data)


@app.route("/ordens/<id>")
def ver_ordem(id):
    response = requests.get(f"{API_URL}/ordens/{id}")
    ordem = response.json() if response.status_code == 200 else {}
    clientes_data = get_api_data("clientes")
    clientes_map = {c["id"]: c["nome"] for c in clientes_data if isinstance(c, dict)}
    if isinstance(ordem, dict):
        ordem["cliente_nome"] = clientes_map.get(ordem.get("cliente_id"), "Desconhecido")
    return render_template("ver_ordem.html", ordem=ordem)


@app.route("/ordens/editar/<id>", methods=["GET", "POST"])
def editar_ordem(id):
    if request.method == "POST":
        data = {
            "equipamento": request.form.get("equipamento", ""),
            "problema": request.form.get("descricao_problema", ""),
            "solucao": request.form.get("solucao", ""),
            "status": request.form.get("status", "aberta")
        }
        requests.put(f"{API_URL}/ordens/{id}", json=data)
        return redirect("/ordens")

    response = requests.get(f"{API_URL}/ordens/{id}")
    ordem = response.json() if response.status_code == 200 else {}
    clientes_data = get_api_data("clientes")
    return render_template("editar_ordem.html", ordem=ordem, clientes=clientes_data)


@app.route("/ordens/deletar/<id>")
def deletar_ordem(id):
    requests.delete(f"{API_URL}/ordens/{id}")
    return redirect("/ordens")


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
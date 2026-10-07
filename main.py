from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Clientes, Produtos, Vendas, ItemVenda
from datetime import datetime, timezone
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    clientes = db.session.query(Clientes).all()

    return render_template('index.html', clientes=clientes)

# ----------------------------------------------------------------------------------------------------------------

# HUB Registros de Dados
@app.route("/data_register")
def registro_dados():

    return render_template('registrar.html')

# Registro de Clientes
@app.route("/client_register",methods=['GET','POST'])
def registrar_cliente():

    if request.method == 'POST':
        nome = request.form['nomeClienteForm']
        email = request.form['emailForm']
        telefone = request.form['telefoneForm']

        novoCliente = Clientes(nome_cliente=nome, email=email, telefone=telefone)
        db.session.add(novoCliente)
        db.session.commit()

        return render_template("registrar_cliente.html", sucesso=True)

    return render_template("registrar_cliente.html")

# Registro de Produtos
@app.route("/product_register",methods=['GET','POST'])
def registrar_produto():

    if request.method == 'POST':
        nome = request.form['nomeProdutoForm']
        preco = request.form['preçoProdutoForm']
        estoque = request.form['estoqueProdutoForm']

        novoProduto = Produtos(nome_produto=nome, preco_produto=preco, estoque=estoque)
        db.session.add(novoProduto)
        db.session.commit()

        return render_template("registrar_produto.html", sucesso=True)

    return render_template("registrar_produto.html")

# Registro de Vendas
@app.route("/sale_register",methods=['GET','POST'])
def registrar_venda():

    clientes_brutos = Clientes.query.all()
    clientes_unicos = {c.nome_cliente: c for c in clientes_brutos}.values()
    lista_produtos = Produtos.query.all()

    if request.method == 'POST':
        id_cliente = request.form['idClienteForm']
        detalhes = request.form['detalhesForm']

        data_str = request.form.get('dataVendaForm')
        if data_str:
            data_convertida = datetime.strptime(data_str, '%Y-%m-%d')
        else:
            data_convertida = datetime.now(timezone.utc)

        produtos_ids = request.form['idProdutoForm[]']
        quantidades = request.form['quantidadeForm[]']

        novaVenda = Vendas(
            id_cliente = id_cliente,
            data_venda = data_convertida,
            detalhes = detalhes
        )
        db.session.add(novaVenda)
        db.session.commit

        for prod_id, qtd in zip(produtos_ids, quantidades):
            if not prod_id or not qtd:
                continue

            qtd_int = int(qtd)
            produto = Produtos.query.get(prod_id)

            produto.estoque -= qtd_int

            item = ItemVenda(
                id_venda = novaVenda.id_venda,
                id_produto = produto.id_produto,
                quantidade_produto = qtd_int
            )
            db.session.add(item)

        db.session.commit()

        return render_template("registrar_venda.html", sucesso=True, clientes = clientes_unicos, produtos = lista_produtos)


    return render_template("registrar_venda.html", clientes=clientes_unicos, produtos=lista_produtos)

# ----------------------------------------------------------------------------------------------------------------

# HUB Visualização de Dados
@app.route("/data_view")
def listar_dados():

    return render_template("visualizar.html")

# Listagem de Clientes
@app.route("/client_view", methods=["GET","POST"])
def listar_clientes():

    criterio_ordCliente = request.args.get('ordenarCli', 'id')
    direcao_ordCliente = request.args.get('direcaoCli', 'asc')

    query_clientes = Clientes.query
    if criterio_ordCliente == 'nome':
        coluna_cli = Clientes.nome_cliente
    else:
        coluna_cli = Clientes.id_cliente

    if direcao_ordCliente == 'desc':
        lista_clientes = query_clientes.order_by(coluna_cli.desc()).all()
    else:
        lista_clientes = query_clientes.order_by(coluna_cli.asc()).all()

    return render_template("visualizar_clientes.html", clientes=lista_clientes)

# Listagem de Produtos
@app.route("/product_view/", methods=["GET","POST"])
def listar_produtos():
    criterio_ordProd = request.args.get('ordenarProd', 'id')
    direcao_ordProd = request.args.get('direcaoProd', 'asc')

    query_produtos = Produtos.query
    if criterio_ordProd == 'nome':
        coluna_prod = Produtos.nome_produto
    elif criterio_ordProd == 'preco':
        coluna_prod = Produtos.preco_produto
    elif criterio_ordProd == 'estoque':
        coluna_prod = Produtos.estoque
    else:
        coluna_prod = Produtos.id_produto

    if direcao_ordProd == 'desc':
        lista_produtos = query_produtos.order_by(coluna_prod.desc()).all()
    else:
        lista_produtos = query_produtos.order_by(coluna_prod.asc()).all()

    return render_template("visualizar_produtos.html", produtos=lista_produtos)

# Listagem de Vendas
@app.route("/sale_view", methods=["GET","POST"])
def listar_vendas():
    criterio_ordProd = request.args.get('ordenarProd', 'id')
    direcao_ordProd = request.args.get('direcaoProd', 'asc')

    query_produtos = Produtos.query
    if criterio_ordProd == 'nome':
        coluna_prod = Produtos.nome_produto
    elif criterio_ordProd == 'preco':
        coluna_prod = Produtos.preco_produto
    elif criterio_ordProd == 'estoque':
        coluna_prod = Produtos.estoque
    else:
        coluna_prod = Produtos.id_produto

    if direcao_ordProd == 'desc':
        lista_produtos = query_produtos.order_by(coluna_prod.desc()).all()
    else:
        lista_produtos = query_produtos.order_by(coluna_prod.asc()).all()

    return render_template("visualizar_produtos.html", produtos=lista_produtos)

# ----------------------------------------------------------------------------------------------------------------

# HUB Edição de Dados
@app.route("/data_edit/", methods=['GET','POST'])
def editar_dados():

    # cliente = db.session.query(Clientes).filter(Clientes.id==id).first()

    return render_template("atualizar.html")

# ----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)






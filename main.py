from flask import Flask, render_template, request, redirect, url_for
from db import db
from sqlalchemy import func
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

        produtos_ids = request.form.getlist('idProdutoForm[]')
        quantidades = request.form.getlist('quantidadeForm[]')

        novaVenda = Vendas(
            id_cliente = id_cliente,
            data_venda = data_convertida,
            detalhes = detalhes
        )
        db.session.add(novaVenda)

        for prod_id, qtd in zip(produtos_ids, quantidades):
            if not prod_id or not qtd:
                continue

            prod_id_int = int(prod_id)
            qtd_int = int(qtd)
            produto = Produtos.query.get(prod_id)

            if not produto:
                continue

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
def editar_dados():

    return render_template("editar.html")

# Edição de Clientes
@app.route("/client_view", methods=["GET","POST"])
def editar_clientes():
    criterio_ordCliente = request.args.get('ordenarCli', 'id')
    direcao_ordCliente = request.args.get('direcaoCli', 'asc')

    query_clientes = Clientes.query

    if criterio_ordCliente == 'nome':
        # Usa func.lower() para ordenar ignorando maiúsculas/minúsculas
        coluna_cli = func.lower(Clientes.nome_cliente)
    else:
        coluna_cli = Clientes.id_cliente

    if direcao_ordCliente == 'desc':
        lista_clientes = query_clientes.order_by(coluna_cli.desc()).all()
    else:
        lista_clientes = query_clientes.order_by(coluna_cli.asc()).all()

    return render_template("editar_clientes.html", clientes=lista_clientes)

# Edição de Produtos
@app.route("/product_view/", methods=["GET","POST"])
def editar_produtos():
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

    return render_template("editar_produtos.html", produtos=lista_produtos)

# Edição de Vendas
@app.route("/sale_view", methods=["GET","POST"])
def editar_vendas():
    criterio_ordVenda = request.args.get('ordenarVenda', 'id')
    direcao_ordVenda = request.args.get('direcaoVenda', 'asc')
    reverso = (direcao_ordVenda == 'desc')

    if criterio_ordVenda == 'data':
        lista_vendas = Vendas.query.order_by(Vendas.data_venda.desc()
            if reverso else Vendas.data_venda.asc()).all()
    elif criterio_ordVenda == 'cliente':
        lista_vendas = Vendas.query.join(Clientes).order_by(Clientes.nome_cliente.desc()
            if reverso else Clientes.nome_cliente.asc()).all()
    elif criterio_ordVenda == 'valor':
        lista_vendas = Vendas.query.all()
        lista_vendas = sorted(lista_vendas, key=lambda v: v.valor_total, reverse=reverso)
    elif criterio_ordVenda == 'quantidade':
        lista_vendas = Vendas.query.all()
        lista_vendas = sorted(lista_vendas, key=lambda v: v.quantidade_total, reverse=reverso)
    else:
        coluna_venda = Vendas.id_venda
        lista_vendas = Vendas.query.order_by(coluna_venda.desc()
            if reverso else coluna_venda.asc()).all()

    return render_template("editar_vendas.html", vendas=lista_vendas)

# ----------------------------------------------------------------------------------------------------------------

# Página de Edição do Cliente
@app.route("/editar_cliente/<int:id>", methods=['GET', 'POST'])
def editar_cliente_form(id):
    cliente = Clientes.query.get_or_404(id)

    if request.method == 'POST':
        # 2. Atualizar os atributos do produto com os dados enviados pelo formulário
        cliente.nome_cliente = request.form.get('nomeClienteForm')
        cliente.email = request.form.get('emailForm') # Ajusta para o name do teu input de preço
        cliente.telefone = request.form.get('telefoneForm')  # Ajusta para o name do teu input de estoque

        # 3. Guardar as alterações na base de dados
        db.session.commit()

        # 4. Redirecionar de volta para a listagem de produtos
        return redirect(url_for('editar_clientes'))

    return render_template("edição_cliente.html", cliente=cliente)

# Página de Edição do Produto
@app.route("/editar_produto/<int:id>", methods=['GET', 'POST'])
def editar_produto_form(id):
    produto = Produtos.query.get_or_404(id)

    if request.method == 'POST':
        # 2. Atualizar os atributos do produto com os dados enviados pelo formulário
        produto.nome_produto = request.form.get('nomeProdutoForm')
        produto.preco_produto = float(request.form.get('preçoProdutoForm'))  # Ajusta para o name do teu input de preço
        produto.estoque = int(request.form.get('estoqueProdutoForm'))  # Ajusta para o name do teu input de estoque

        # 3. Guardar as alterações na base de dados
        db.session.commit()

        # 4. Redirecionar de volta para a listagem de produtos
        return redirect(url_for('editar_produtos'))

    return render_template("edição_produto.html", produto=produto)


# Página de Edição do Pedido
@app.route("/editar_venda/<int:id>", methods=['GET', 'POST'])
def editar_venda_form(id):
    venda = Vendas.query.get_or_404(id)
    clientes = Clientes.query.all()
    produtos = Produtos.query.all()

    if request.method == 'POST':
        # 1. Estornar (devolver) o stock dos itens antigos antes de alterar
        for item in venda.itens:
            prod = Produtos.query.get(item.id_produto)
            if prod:
                prod.estoque += item.quantidade_produto

        # 2. Atualizar os dados gerais da venda
        venda.id_cliente = request.form.get('id_cliente')
        venda.detalhes = request.form.get('detalhes', '')

        # Remover os itens antigos da base de dados
        for item in venda.itens:
            db.session.delete(item)

        # 3. Recolher os novos itens enviados pelo formulário
        produto_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')

        novos_itens = []
        for p_id, qtd in zip(produto_ids, quantidades):
            if p_id and qtd:
                p_id = int(p_id)
                qtd = int(qtd)
                prod = Produtos.query.get(p_id)
                if prod:
                    # Abater o novo stock
                    prod.estoque -= qtd

                    novo_item = ItemVenda(
                        id_venda=venda.id_venda,
                        id_produto=p_id,
                        quantidade_produto=qtd
                    )
                    novos_itens.append(novo_item)

        venda.itens = novos_itens
        db.session.commit()

        return redirect(url_for('editar_vendas'))

    return render_template("edição_venda.html", venda=venda, clientes=clientes, produtos=produtos)

# ----------------------------------------------------------------------------------------------------------------

# Excluir Produto
@app.route("/deletar_cliente/<int:id>")
def excluir_cliente(id):
    cliente = Clientes.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for('editar_clientes'))

# Excluir Produto
@app.route("/deletar_produto/<int:id>")
def excluir_produto(id):
    produto = Produtos.query.get_or_404(id)

    db.session.delete(produto)
    db.session.commit()

    return redirect(url_for('editar_produtos'))

# Excluir Venda
@app.route("/deletar_venda/<int:id>")
def excluir_venda(id):
    venda = Vendas.query.get_or_404(id)

    # Opcional mas recomendado: Devolver os itens ao estoque antes de apagar
    for item in venda.itens:
        produto = Produtos.query.get(item.id_produto)
        if produto:
            produto.estoque += item.quantidade_produto

    # Remove os itens associados e a venda
    for item in venda.itens:
        db.session.delete(item)

    db.session.delete(venda)
    db.session.commit()

    return redirect(url_for('editar_vendas'))

# ----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)






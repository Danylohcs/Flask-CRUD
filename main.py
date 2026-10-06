from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Clientes, Produtos, Vendas
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    clientes = db.session.query(Clientes).all()

    return render_template('index.html', clientes=clientes)

# HUB Registros de Dados
@app.route("/data_register")
def registro_dados():

    return render_template('registrar.html')

# Registro de Clientes
@app.route("/client_register",methods=['GET','POST'])
def registrar_cliente():

    if request.method == 'GET':
        return render_template("registrar_cliente.html")
    elif request.method == 'POST':
        nome = request.form['nomeClienteForm']
        email = request.form['emailForm']
        telefone = request.form['telefoneForm']

        novoCliente = Clientes(nome_cliente=nome, email=email, telefone=telefone)
        db.session.add(novoCliente)
        db.session.commit()

    return redirect(url_for('registro_dados', sucesso=True))

# Registro de Produtos
@app.route("/product_register",methods=['GET','POST'])
def registrar_produto():

    return render_template("registrar_produto.html")

# Registro de Vendas
@app.route("/sale_register",methods=['GET','POST'])
def registrar_venda():

    return render_template("sale_register.html")

# HUB Visualização de Dados
@app.route("/data_view", methods=['GET','POST'])
def listar_dados():
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

    criterio_ordProduto = request.args.get('ordenarProd', 'id')
    direcao_ordProduto = request.args.get('direcaoProd', 'asc')

    criterio_ordVenda = request.args.get('ordenarVenda', 'id')
    direcao_ordVenda = request.args.get('direcaoVenda', 'asc')

    lista_produtos = Produtos.query.all()
    lista_vendas = Vendas.query.all()

    return render_template("visualizar.html", clientes=lista_clientes,produtos=lista_produtos,vendas=lista_vendas)

# HUB Edição de Dados
@app.route("/data_edit/", methods=['GET','POST'])
def editar_dados():

    # cliente = db.session.query(Clientes).filter(Clientes.id==id).first()

    return render_template("atualizar.html")

# HUB Exclusão de Dados
@app.route("/data_delete/", methods=["GET","POST"])
def deletar_dados():

    # cliente = db.session.query(Clientes).filter(Clientes.id==id).first()
    # db.session.delete(cliente)
    # db.session.commit()

    return render_template("deletar.html")

if __name__ == "__main__":
    app.run(debug=True)






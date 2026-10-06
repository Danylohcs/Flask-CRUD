from db import db

class Clientes(db.Model):
    __tablename__ = 'Clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

    def __repr__(self):
        return f"<Cliente {self.nome_cliente}>"

class Produtos(db.Model):
    __tablename__ = 'Produtos'

    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(80), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

class Vendas(db.Model):
    __tablename__ = 'Vendas'

    id_venda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('Clientes.id_cliente'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('Produtos.id_produto'), nullable=False)
    detalhes = db.Column(db.String(256))
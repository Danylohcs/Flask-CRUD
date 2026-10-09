from db import db

class Clientes(db.Model):
    __tablename__ = 'Clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

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
    detalhes = db.Column(db.String(256))
    data_venda = db.Column(db.DateTime, nullable=False)

    cliente = db.relationship('Clientes', backref='vendas')

    itens = db.relationship('ItemVenda', backref='venda', cascade='all, delete-orphan')

    @property
    def valor_total(self):
        return sum(item.quantidade_produto * item.produto.preco_produto for item in self.itens)

    @property
    def quantidade_total(self):
        return sum(item.quantidade_produto for item in self.itens)

class ItemVenda(db.Model):
    __tablename__ = 'ItemVenda'

    id_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venda = db.Column(db.Integer, db.ForeignKey('Vendas.id_venda'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('Produtos.id_produto'), nullable=False)
    quantidade_produto = db.Column(db.Integer, nullable=False)

    produto = db.relationship('Produtos')
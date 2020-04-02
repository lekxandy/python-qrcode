from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = '12344321'

db = SQLAlchemy(app)

admin = Admin(app)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    matricula = db.Column(db.String(8))

    def __str__(self):
        return self.nome

class Formacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String(255))
    data = db.Column(db.Date)
    carga_horaria = db.Column(db.Integer)

    def __str__(self):
        return self.tema

class Certificado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))
    formacao_id = db.Column(db.Integer, db.ForeignKey('formacao.id'))
    formacao = db.relationship('Formacao')
    pessoa = db.relationship('Pessoa')

    def __str__(self):
        return '{} - {}'.format(self.pessoa, self.formacao)

@app.route('/validar/<string:codigo>')
def validar(codigo):
    certificados = Certificado.query.all()
    for c in certificados:
        cod = '{}{}{}{}'.format(c.id, c.pessoa_id, c.pessoa.matricula, c.formacao_id)
        print(cod)
        if codigo == cod:
            return "Válido: Matrícula: {} \nPessoa: {} \nFormação: {} \nData: {} ".format(cod[3:8],c.pessoa,c.formacao,c.formacao.data)
    return "Inválido"

@app.route('/certificado/<int:id>')
def certificados_pessoa(id):
    certificado = Certificado.query.get(id)
    cod = '{}{}{}{}'.format(certificado.id, certificado.pessoa_id, certificado.pessoa.matricula, certificado.formacao_id)

    return render_template('certificado.html', certificado=certificado, cod=cod)

admin.add_view(ModelView(Pessoa, db.session))
admin.add_view(ModelView(Formacao, db.session))
admin.add_view(ModelView(Certificado, db.session))

if __name__=='__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
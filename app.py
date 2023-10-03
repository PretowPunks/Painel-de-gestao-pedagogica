from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
db = SQLAlchemy(app)

# Configurações e definições do SQLAlchemy, LoginManager, classes de modelos, etc.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:#pretowDBApass1989@localhost/db_eecruzeiro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Defina uma chave secreta para o Flask


login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Defina a classe do usuário com UserMixin
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

@login_manager.user_loader
def load_user(user_id):
    # Função necessária para o login_manager carregar o usuário da sessão
    return db.session.get(Usuario, int(user_id))

class PlanoAula(db.Model):
    __tablename__ = 'plano_aula'
    id = db.Column(db.Integer, primary_key=True)
    professor = db.Column(db.String(100), nullable=False)
    area_conhecimento = db.Column(db.String(100), nullable=False)
    componente_curricular = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(100), nullable=False)
    objetivos = db.Column(db.Text, nullable=False)
    objeto_estudo = db.Column(db.Text, nullable=False)
    habilidades = db.Column(db.Text, nullable=False)
    num_aulas = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    atividades = db.Column(db.Text, nullable=False)
    recursos = db.Column(db.Text, nullable=False)
    avaliacao = db.Column(db.Text, nullable=False)
    devolutiva = db.Column(db.Text, nullable=False)

    def __init__(self, professor, area_conhecimento, componente_curricular, turma, objetivos, objeto_estudo, habilidades, num_aulas, data_inicio, atividades, recursos, avaliacao, devolutiva):
        self.professor = professor
        self.area_conhecimento = area_conhecimento
        self.componente_curricular = componente_curricular
        self.turma = turma
        self.objetivos = objetivos
        self.objeto_estudo = objeto_estudo
        self.habilidades = habilidades
        self.num_aulas = num_aulas
        self.data_inicio = data_inicio
        self.atividades = atividades
        self.recursos = recursos
        self.avaliacao = avaliacao
        self.devolutiva = devolutiva

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', nome_usuario=current_user.nome if current_user.is_authenticated else '')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            login_user(usuario)  # Faz login do usuário
            return redirect(url_for('planos_de_aula'))

        return render_template('loginfail.html')

    return render_template('login.html')

@app.route('/loginfail', methods=['GET','POST'])
def login_fail():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email,senha=senha)
        if usuario:
            login_user(usuario)
            return redirect(url_for('planos_de_aula'))
    
    return render_template('loginfail.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()  # Faz logout do usuário
    return redirect(url_for('index'))

@app.route('/novo_usuario', methods=['GET', 'POST'])
def novo_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        email_existente = Usuario.query.filter_by(email=email).first()
        nome_existente = Usuario.query.filter_by(nome=nome).first()
        if email_existente or nome_existente:
            return render_template('cadfail.html')

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('novo_usuario.html')

@app.route('/planos_de_aula', methods=['GET', 'POST'])
@login_required
def planos_de_aula():
    planos = PlanoAula.query.all()
    professores = list(set([plano.professor for plano in planos]))
    turmas = list(set([plano.turma for plano in planos]))
    componentes = list(set([plano.componente_curricular for plano in planos]))
    datas = list(set([plano.data_inicio for plano in planos]))

    return render_template('planos_de_aula.html', planos=planos, nome_usuario=current_user.nome, professores=professores, turmas=turmas, componentes=componentes, datas=datas)

@app.route('/novoplano', methods=['GET', 'POST'])
@login_required
def novoplano():
    if request.method == 'POST':
        professor = request.form.get('professor')
        area_conhecimento = request.form.get('area_conhecimento')
        componente_curricular = request.form.get('componente_curricular')
        turma = request.form.get('turma')
        objetivos = request.form.get('objetivos')
        objeto_estudo = request.form.get('objeto_estudo')
        habilidades = request.form.get('habilidades')
        num_aulas = int(request.form.get('num_aulas'))
        data_inicio = request.form.get('data_inicio')
        atividades = request.form.get('atividades')
        recursos = request.form.get('recursos')
        avaliacao = request.form.get('avaliacao')
        devolutiva = request.form.get('devolutiva')

        novo_plano_aula = PlanoAula(professor=professor, area_conhecimento=area_conhecimento,
                                   componente_curricular=componente_curricular, turma=turma, objetivos=objetivos,
                                   objeto_estudo=objeto_estudo, habilidades=habilidades, num_aulas=num_aulas,
                                   data_inicio=data_inicio, atividades=atividades, recursos=recursos,
                                   avaliacao=avaliacao, devolutiva=devolutiva)

        db.session.add(novo_plano_aula)
        db.session.commit()

        return redirect(url_for('planos_de_aula'))

    return render_template('novo_plano.html')

@app.route('/view/<int:plano_id>', methods=['GET', 'POST'])
@login_required
def view(plano_id):
    plano = PlanoAula.query.get(plano_id)
    if not plano:
        return render_template('view.html', error_message='Plano não encontrado.')

    return render_template('view.html', plano=plano)

@app.route('/excluir_plano/<int:plano_id>', methods=['POST', 'DELETE'])
@login_required
def excluir_plano(plano_id):
    plano = PlanoAula.query.get(plano_id)
    if not plano:
        return redirect(url_for('planos_de_aula'))

    # Realize a lógica de exclusão do plano aqui (por exemplo, usando o SQLAlchemy)
    # Exemplo de código para excluir o plano:
    db.session.delete(plano)
    db.session.commit()

    return redirect(url_for('planos_de_aula'))

@app.route('/editar_plano/<int:plano_id>', methods=['GET', 'POST'])
@login_required
def editar_plano(plano_id):
    plano = PlanoAula.query.get(plano_id)
    if not plano:
        return render_template('editar_plano.html', error_message='Plano não encontrado.')

    if request.method == 'POST':
        # Obter os dados do formulário enviado
        professor = request.form.get('professor')
        area_conhecimento = request.form.get('area_conhecimento')
        componente_curricular = request.form.get('componente_curricular')
        turma = request.form.get('turma')
        objetivos = request.form.get('objetivos')
        objeto_estudo = request.form.get('objeto_estudo')
        habilidades = request.form.get('habilidades')
        num_aulas = int(request.form.get('num_aulas'))
        data_inicio = request.form.get('data_inicio')
        atividades = request.form.get('atividades')
        recursos = request.form.get('recursos')
        avaliacao = request.form.get('avaliacao')
        devolutiva = request.form.get('devolutiva')

        # Atualiza os atributos do plano de aula com os novos valores
        plano.professor = professor
        plano.area_conhecimento = area_conhecimento
        plano.componente_curricular = componente_curricular
        plano.turma = turma
        plano.objetivos = objetivos
        plano.objeto_estudo = objeto_estudo
        plano.habilidades = habilidades
        plano.num_aulas = num_aulas
        plano.data_inicio = data_inicio
        plano.atividades = atividades
        plano.recursos = recursos
        plano.avaliacao = avaliacao
        plano.devolutiva = devolutiva

        # Salva as alterações no banco de dados
        db.session.commit()

        # Redireciona para a página de visualização do plano de aula atualizado
        return redirect(url_for('view', plano_id=plano.id))

    return render_template('editar_plano.html', plano=plano)


if __name__ == '__main__':
    app.run(debug=True)

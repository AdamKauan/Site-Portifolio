from flask import Flask, render_template, request, redirect, flash, session, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Adamkauan.'
# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DMM\\SQLMATIAS/DBSITE?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

app.config['SQLALCHEMY_ECHO'] = True

# Modelo para a tabela 'contatos'
class Contato(db.Model):
    __tablename__ = 'contatos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.now)

# Função para garantir que as tabelas sejam criadas
def create_db():
    # Se as tabelas ainda não existirem, cria-as
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")

# Função para corrigir o próximo ID após exclusão
def reset_id():
    with app.app_context():
        # Recalcula o próximo ID para o campo auto increment (SQL Server)
        db.session.execute('DBCC CHECKIDENT ("contatos", RESEED)')  # Reseta o contador de IDs
        db.session.commit()

# Rota principal para exibir o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário de contato
@app.route('/send', methods=['POST'])
def send():
    try:
        # Capturar os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        # Validar os campos
        if not nome or not email or not mensagem:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect('/')

        # Criar um novo registro de contato
        novo_contato = Contato(nome=nome, email=email, mensagem=mensagem)

        # Adicionar ao banco de dados
        db.session.add(novo_contato)
        db.session.commit()

        # Mensagem de sucesso
        flash("Mensagem enviada com sucesso!", "success")
        return redirect('/#contato')
    except Exception as e:
        # Mensagem de erro em caso de exceção
        flash(f"Ocorreu um erro: {str(e)}", "error")
        return redirect('/#contato')

# Rota para exibir a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar se o usuário já está logado
    if session.get('logged_in'):
        return redirect(url_for('relatorio'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Login simples com usuário e senha fixos
        if username == 'admin' and password == 'Adamkauan.':  # Substitua pela sua senha
            session['logged_in'] = True
            return redirect(url_for('relatorio'))
        else:
            flash('Usuário ou senha inválidos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota protegida para exibir o relatório de contatos com paginação
@app.route('/relatorio')
def relatorio():
    if not session.get('logged_in'):  # Verifica se o usuário está logado
        flash('Você precisa fazer login para acessar esta página', 'danger')
        return redirect(url_for('login'))
    
    # Obter a página atual a partir dos parâmetros de URL, padrão para 1
    page = request.args.get('page', 1, type=int)

    # Consulta os dados com paginação
    contatos = Contato.query.order_by(Contato.data_envio.desc()).paginate(page=page, per_page=10)

    # Impede o cache das páginas protegidas (também para evitar que o navegador permita voltar à página após o logout)
    response = make_response(render_template('relatorio.html', contatos=contatos))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

# Rota para logout
@app.route('/logout')
def logout():
    # Remove a sessão de login
    session.pop('logged_in', None)
    flash('Você saiu da conta', 'success')
    return redirect(url_for('login'))

# Rota para excluir um contato
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    contato = Contato.query.get_or_404(id)
    db.session.delete(contato)
    db.session.commit()

    # Após a exclusão, chamar a função para resetar o ID
    reset_id()

    flash(f'Contato {id} deletado com sucesso!', 'success')
    return redirect(url_for('relatorio'))

# Inicializar tabelas e rodar o servidor
if __name__ == '__main__':
    # Rodar o servidor Flask
    create_db()  # Chama a função para criar as tabelas
    app.run(debug=True, use_reloader=True)

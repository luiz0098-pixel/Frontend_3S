from datetime import datetime

from flask import Flask, render_template, url_for, flash, request, redirect
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Funcionario
from sqlalchemy import select, and_, func
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    user = select(Funcionario).where(Funcionario.id == int(user_id))
    resultado = db_session.execute(user).scalar_one_or_none()
    return resultado


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # pega o campo do formulario
        email = request.form['form-email']
        senha = request.form['form-senha']

        if not email or not senha:
            flash('Por favor preencher todos os campos', 'alert-danger')
            return render_template('login.html')

        if email and senha:
            email_sql = select(Funcionario).where(Funcionario.email == email)
            resultado_email = db_session.execute(email_sql).scalar_one_or_none()

            if resultado_email:
                if resultado_email.check_password(senha):
                    # Realiza a autenticação
                    login_user(resultado_email)
                    flash(f'logado com sucesso!', 'success')

                    return redirect(url_for('home'))
                else:
                    # login incorreto
                    flash('senha incorreto', 'danger')
                    return render_template('login.html')

            else:
                flash(f'Email nao encontrado', 'alert-danger')
                return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('logout com sucesso!', 'success')
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        data = datetime.strptime(request.form.get('form-data'), '%Y-%m-%d')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        cargo = request.form.get('form-cargo')
        cpf = request.form.get('form-cpf')
        salario = float(request.form.get('form-salario'))

        if not nome or not email or not senha:
            flash('Por favor preencher os campos', 'danger')
            return render_template('funcionarios.html')

        verifica_email = select(Funcionario).where(Funcionario.email == email)
        existe_email = db_session.execute(verifica_email).scalar_one_or_none()

        if existe_email:
            flash(f'Email {email} ja esta cadastrado', 'danger')
            return render_template('funcionarios.html')
        try:
            novo_funcionario = Funcionario(nome=nome, email=email, senha=senha, data_nasc=data, cargo=cargo,
                                           salario=salario, cpf=cpf)
            novo_funcionario.set_password(senha)
            db_session.add(novo_funcionario)
            db_session.commit()
            flash(f'funcionario {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))

        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar funcionario', 'danger')
            print(f'Erro na base de dados: {e}')
            return redirect(url_for('cadastro_funcionario'))

        except Exception as e:
            flash(f'Erro ao cadastrar funcionario', 'danger')
            print(f'Erro ao cadastrar funcionario: {e}')
            return redirect(url_for('cadastro.funcionario'))
    return render_template('funcionarios.html')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/calculos')
def calculos():
    return render_template("calculos.html")


@app.route('/operacoes')
def operacoes():
    return render_template("operacoes.html")


@app.route('/geometria')
def geometria():
    return render_template("geometria.html")


@app.route('/funcionarios')
@login_required
def funcionarios():
    func_sql = select(Funcionario)
    resultado = db_session.execute(func_sql).scalars().all()
    return render_template("funcionarios.html", resultado=resultado)


@app.route('/somar', methods=['GET', 'POST'])
def somar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            soma = n1 + n2
            flash("soma realizada", "alert-success")
            return render_template("operacoes.html", n1=n1, n2=n2, soma=soma)
        else:
            flash("Preencha o campo para realizar a soma", 'alert-danger')
    return render_template("operacoes.html")


@app.route('/subtrair', methods=['GET', 'POST'])
def subtrair():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            subtracao = n1 - n2
            flash("soma realizada", "alert-success")
            return render_template("operacoes.html", n1=n1, n2=n2, subtracao=subtracao)
        else:
            flash("Preencha o campo para realizar a soma", 'alert-danger')
    return render_template("operacoes.html")


@app.route('/multiplicacao', methods=['GET', 'POST'])
def multiplicar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            multiplicacao = n1 * n2
            flash("soma realizada", "alert-success")
            return render_template("operacoes.html", n1=n1, n2=n2, multiplicacao=multiplicacao)
        else:
            flash("Preencha o campo para realizar a soma", 'alert-danger')
    return render_template("operacoes.html")


@app.route('/divisao', methods=['GET', 'POST'])
def dividir():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            divisao = n1 / n2
            flash("soma realizada", "alert-success")
            return render_template("operacoes.html", n1=n1, n2=n2, divisao=divisao)
        else:
            flash("Preencha o campo para realizar a soma", 'alert-danger')
    return render_template("operacoes.html")


# TODO Final do código

@app.route('/triangulo_area', methods=['GET', 'POST'])
def triangulo_area():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            triangulo_area = n1 * n2 / 2
            flash("area realizada", "alert-success")
            return render_template("geometria.html", n1=n1, n2=n2, triangulo_area=triangulo_area)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/triangulo_perimetro', methods=['GET', 'POST'])
def triangulo_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            triangulo_perimetro = n1 * 3
            flash("perimetro realizado", "alert-success")
            return render_template("geometria.html", n1=n1, triangulo_perimetro=triangulo_perimetro)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/circulo_area', methods=['GET', 'POST'])
def circulo_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            circulo_area = 3.14 * n1 ** 2
            flash("area realizada", "alert-success")
            return render_template("geometria.html", n1=n1, circulo_area=circulo_area)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/circulo_perimetro', methods=['GET', 'POST'])
def circulo_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            circulo_perimetro = n1 ** 2 * 3.14
            flash("perimetro realizado", "alert-success")
            return render_template("geometria.html", n1=n1, circulo_perimetro=circulo_perimetro)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/quadrado_area', methods=['GET', 'POST'])
def quadrado_area():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            quadrado_area = n1 * n1
            flash("area realizada", "alert-success")
            return render_template("geometria.html", n1=n1, quadrado_area=quadrado_area)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/quadrado_perimetro', methods=['GET', 'POST'])
def quadrado_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            quadrado_perimetro = n1 * 4
            flash("perimetro realizado", "alert-success")
            return render_template("geometria.html", n1=n1, quadrado_perimetro=quadrado_perimetro)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/hexagono_area', methods=['GET', 'POST'])
def hexagono_area():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            hexagono_area = n1 * n2 / 2 * 6
            flash("area realizada", "alert-success")
            return render_template("geometria.html", n1=n1, n2=n2, hexagono_area=hexagono_area)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


@app.route('/hexagono_perimetro', methods=['GET', 'POST'])
def hexagono_perimetro():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            hexagono_perimetro = n1 * 6
            flash("perimetro realizado", "alert-success")
            return render_template("geometria.html", n1=n1, hexagono_perimetro=hexagono_perimetro)
        else:
            flash("Preencha o campo", "alert-danger")
    return render_template("geometria.html")


if __name__ == '__main__':
    app.run(debug=True)

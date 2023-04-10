from flask import Flask, render_template, request, redirect, url_for,jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SECRET_KEY'] = 'Maicon2018$' 



#-------Area de pagamentos-------


# SDK do Mercado Pago
import mercadopago
from random import choice
# Configure as credenciais

sdk = mercadopago.SDK("APP_USR-4368628010042942-091321-5f0f7612469859189ef6c95d2aab3156-1165943682")


def Create_payment():
    preference_data = {
        "items": [
            {
                "title": "Assinatura +1 mes bot-sala",
                "quantity": 1,
                'id': str([choice('w s x 0 i d o - = ! 8 2 0 8 d x - = ! d j d a f 0 9 2 7 3 = - y e x ! d m s *'.split(' ')) for x in range(20)]),
                "unit_price": 49.90
            }
        ]
    }


    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    preference_id = preference['items'][0]['id']
    collector_id = preference['collector_id']
    url = preference['init_point']

    print(url)
    return preference


def get_peyment(collector_id):
    result = sdk.payment().search()
    result = result['response']['results']
    for c in result:
        if c['additional_info']['items'][0]['id'] == collector_id:
            return c['status'] == 'approved'
# -----fim dos pagamentos-------


# send email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USERNAME = "maisantosmix2018@hotmail.com"
SMTP_PASSWORD = "Negucio2018$"

EMAIL_FROM = "maisantosmix2018@hotmail.com"

def send_email(EMAIL_TO):
    code = ''
    for c in range(6):
        code += str(choice(range(0, 10)))

    html = '<h1>seu codigo de confirmação botwinner <br><br> codigo: ' + code + '</h1>'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Botwinner - bussines"
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    debuglevel = False


    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
    return code



db = SQLAlchemy()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    
    verify = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)

    free_days = db.Column(db.Integer, nullable=False)
    preference_id = db.Column(db.String)
    collector_id = db.Column(db.String)
    pay_date = db.Column(db.String)
    bot = db.Column(db.String, unique=True, nullable=False)
    data = db.Column(db.String, nullable=False)



def verify_login(email, senha):
    try:
        if len(email) > 0 and len(senha) > 0:

            return True
        return False
    except:
        return False




db.init_app(app)
with app.app_context():
    db.create_all()



@app.route("/")
def lading():
    return render_template('lading.html')

@app.route("/dashboard")
def main():
    try:    
        email = session['email']   
        user = User.query.filter_by(email=email).first()
        
        if user.verify == 'false':
            return redirect(url_for('verify'))
        
        if verify_login(session['email'], session['senha']): 

            #user.pay_date = str(datetime.now()).split(' ')[0]
            #db.session.commit() 

            if user.pay_date == 'false':
                pay_date = datetime.now()
                added_date = str(pay_date + timedelta(days=30)).split(' ')[0]
            else:
                now = datetime.now()
                pay_date = datetime.strptime(user.pay_date.replace('-', ' '), '%Y %m %d')
                added_date = str(pay_date + timedelta(days=32)).split(' ')[0]
                
                

                if now >= pay_date:
                    print('acabou o prazo')
                else:
                    print('ainda tem prrazo')
                

            if len(user.collector_id) > 0:

                if get_peyment(collector_id=user.collector_id):
                    pay_date = datetime.strptime(user.pay_date.replace('-', ' '), '%Y %m %d')

                    added_date = str(datetime.now()).split(' ')[0]
                    

                    user.collector_id = ''
                    user.pay_date = added_date
                    db.session.commit()

            return render_template('index.html',
                                bot_id=user.bot,
                                free_days=user.free_days,
                                pay_date = user.pay_date
                            )
    except Exception as e:
        print(e)
        session['email'] = ''
        session['senha'] = ''


    return redirect(url_for('entrar'))


#peyments methods
@app.route("/pay")
def pay():
    preference = Create_payment()

    collector_id = preference['items'][0]['id']
    url = preference['init_point']

    email = session['email']    
    user = User.query.filter_by(email=email).first()
    user.collector_id = collector_id
    db.session.commit() 

    return redirect(url)






@app.route("/entrar", methods=["POST", 'GET'])
def entrar():
    try:
        
        

        if verify_login(session['email'], session['senha']):
            return redirect(url_for('main'))

        if request.method == 'GET':
            return render_template('login.html')


        email = request.form.get('email').strip()
        senha = request.form.get('password').strip()

        user = User.query.filter_by(email=email).first()
        if user.senha == senha:  
            session['email'] = email
            session['senha'] = senha

            return redirect(url_for('main'))

        return redirect(url_for('entrar'))
    except:
        return redirect(url_for('entrar'))


@app.route("/verify", methods=["POST", 'GET'])
def verify():
    if request.method == 'GET':
        try:
            email = session['email']
            user = User.query.filter_by(email=email).first()
            if user.verify == 'true':
                return redirect(url_for('main'))
            else:
                return render_template('verification.html')


        except:
            return redirect(url_for('main'))
        
    else:         
        try:            
            verify = request.form.get('code').strip()
            email = session['email']    
            user = User.query.filter_by(email=email).first()

            if user.code == verify:
                user.verify = 'true'
                db.session.commit() 

                return redirect(url_for('main'))
            else:
                return render_template('verification.html')

        except:
            return render_template('verification.html')





@app.route("/cad", methods=["POST", 'GET'])
def create_user():
    

    if request.method == 'GET':
        return render_template('cadastro.html')
    try:            
        nome = request.form.get('nome').strip()
        email = request.form.get('email').strip()
        senha = request.form.get('password').strip()
        
        data = str(datetime.now())

        
        pay_date = datetime.now()
        added_date = str(pay_date + timedelta(days=3)).split(' ')[0]




        user = User.query.filter_by(email=email).first()
        if not user:
            code = send_email(email)
        else:
            return redirect(url_for('create_user'))

        user = User(email=email, name=nome, code=code, verify='false', senha=senha, bot='', data=data ,free_days=2, preference_id='', collector_id='', pay_date=added_date)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main'))
    except:
        return redirect(url_for('main'))






@app.route("/update-bot", methods=['POST'])
def updateBot():
        bot_id = request.form.get('bot_id').strip()

        user = User.query.filter_by(email=session['email']).first()
        user.bot = bot_id
        db.session.commit()

        return redirect(url_for('main'))

@app.route("/sair")
def sair():
    session['email'] = ''
    session['senha'] = ''
    return redirect(url_for('entrar'))




app.run(port=5001)

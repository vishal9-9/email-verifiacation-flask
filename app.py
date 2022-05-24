from flask import Flask, request , render_template
from flask_mail import  Mail , Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('helloworld')

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    email = request.form['email']
    token = s.dumps(email,salt=None)  
    msg = Message(subject = 'Confirm Email',sender = 'alexmercerazon@gmail.com',recipients=[email])
    link = "http://127.0.0.1:5000/" + token #use url_for instead
    msg.body = f'your conf link is {link}'
    mail.send(msg)
    return f'the email you entered is {email} and token is {token}'

@app.route('/<token>')
def home(token):
    try:
        email = s.loads(token,max_age = 35)
    except:
        return 'token Expired'
    return 'token works'

if __name__ == '__main__':
    app.run(debug=True) 
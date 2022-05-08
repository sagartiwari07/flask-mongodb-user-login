from flask import Flask, render_template, flash, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from flask_recaptcha import ReCaptcha
from random import randint

app = Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'userlogin'
app.config['MONGO_URI'] = 'mongodb+srv://sangam:<password>1@userlogin.jzluw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

# Email Verification

mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'sagartiwari.bmp@gmail.com'   
app.config['MAIL_PASSWORD'] = '**********'                #App password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)


# Recaptcha Verification

recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6LeKOaMZAAAAAI7L6TVsZa9A2t6-9LDVYSVqX9ZP",
    RECAPTCHA_SECRET_KEY="6LeKOaMZAAAAAKw9nhAjnpzrzrC3R0YYRf-kKDH1",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)


#Routes


mongo = PyMongo(app)


@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')

    return render_template('error.html')



@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email': request.form['email']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['email'] = request.form['email']
            email = request.form['email']
            msg = Message(subject='otp', sender='sagartiwari.bmp@gmail.com', recipients=[email])
            msg.body = str(otp)
            mail.send(msg)
            return render_template('verify.html')

    return render_template('error.html')



@app.route('/validate', methods=['POST'])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp) and recaptcha.verify():
        return render_template('dashboard.html')
    return render_template('error.html')



@app.route('/signout')
def signout():
    return render_template('index.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'userlogin'
app.config['MONGO_URI'] = 'mongodb+srv://sangam:Workinflow1@userlogin.jzluw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'email' in session:
        return render_template('dashboard.html')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['email']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/signout')
def signout():
  return render_template('index.html')    

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
from flask import Flask, request,render_template,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import messagebox

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/flask_db'
app.secret_key = 'super-secret-key'
db=SQLAlchemy(app)

# ---- Todo Configure MAIL SETUP-------------
try:
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT='465',
        MAIL_USE_SSL=True,
        MAIL_USERNAME='Your Mail',
        MAIL_PASSWORD='Your App Password'
    )
    mail=Mail(app)
except Exception as e:
    print(e)


class Credentials(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    email_id=db.Column(db.String, nullable=False)
    username=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('login.html')
    else:
        user=request.form.get('user')
        passw=request.form.get('pass')

        credential = Credentials.query.filter_by(username=user).first()

        if credential and credential!=None:
            if passw==credential.password:
                return "Successfully Login"
            else:
                return 'Password is Incorrect Try Again'
        else:
            return 'User Name is Not Valid!'

@app.route('/resetpas',methods=['GET','POST'])
def resetpassword():
    if request.method=='GET':
        return render_template('resetpas.html')
    else:
        email_user=request.form.get('email')
        pass1=request.form.get('pass1')
        pass2=request.form.get('pass2')

        credential = Credentials.query.filter_by(email_id=email_user).first()
        print(credential)

        if credential and credential!=None:
            if pass1==pass2:
                credential.password=pass2
                db.session.commit()
                return "Password Successfully Resest"
            else:
                return "Password is Not Match Try Again."
        else:
            return "Email is Not Valid"

@app.route('/createaccount',methods=['GET','POST'])
def createaccount():
    if request.method=='GET':
        return render_template('createaccount.html')
    else:
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        password2=request.form.get('password2')

        credentials=Credentials.query.filter_by(username=username).first()
        print(credentials)
        if credentials==None:
            if str(password)==str(password2):
                add_user=Credentials(username=username,email_id=email,password=password2)
                db.session.add(add_user)
                db.session.commit()
                name="Hello"
                mail.send_message('New Message From ' + name,
                                  sender=email,
                                  recipients='your mail',
                                  body='BROOOO'
                                  )
                return "Successfully Register"
            else:
                return "Password is not match"
        else:
            return "User Already In Database"
if __name__=='__main__':
    app.run(debug=True)

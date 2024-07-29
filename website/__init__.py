from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '49119f659b3a928820bd80e2462fdca9942640f89162c97c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2062732:#SBaloch789@csmysql.cs.cf.ac.uk:3306/c2062732_Shaheer'


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from website import routes

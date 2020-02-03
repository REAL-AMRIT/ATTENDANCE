from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel,gettext
from flask import request
from configparser import ConfigParser




#location of database
#URI= 'mysql+pymysql://root:@localhost:3306/aps2'
cfg = ConfigParser()

cfg.read_file(open('configure/cfg.ini'))

URI= cfg.get('database', 'database_uri')


#initializing flask app
app = Flask(__name__)


#configuring the uri
app.config['SQLALCHEMY_DATABASE_URI'] = URI

#initializing the database object
db = SQLAlchemy(app)

#used for protection from modifying cookies
app.secret_key = cfg.get('settings', 'secret_key')


#initializing login manager
login_manager = LoginManager(app)

#redirects to login function if user is not loged in
login_manager.login_view = 'login'


#create association with actual user data in the database
from attendance.models import Employee

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))



app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel =Babel(app)


@babel.localeselector
def get_locale():
    #return 'en'
    return request.accept_languages.best_match(['hi', 'en'])


from attendance import routes
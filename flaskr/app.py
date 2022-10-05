import auth, candidate, recruiter, shared_operation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db_session, db

UPLOAD_FOLDER = '../images/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/JobFinding'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

app.register_blueprint(auth.bp)
app.register_blueprint(candidate.bp)
app.register_blueprint(recruiter.bp)
app.register_blueprint(shared_operation.bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def hello():
    return 'Hey, it worked!'

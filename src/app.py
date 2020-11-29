from apiv1 import blueprint as api1

from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from db import models
from db.service import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

solaris_recognizer_app = Flask(__name__)
CORS(solaris_recognizer_app)
solaris_recognizer_app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
solaris_recognizer_app.register_blueprint(api1)

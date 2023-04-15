import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


dotenv_path = os.path.join(os.getcwd(), ".env")
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv

    load_dotenv(dotenv_path)

app = Flask(__name__)

app.config.from_object(os.environ.get("CONFIG_OBJECT"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

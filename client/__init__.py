from os import getenv
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = '123_user_1544'
API_URL = getenv('API_URL')


from . import routers, utils 
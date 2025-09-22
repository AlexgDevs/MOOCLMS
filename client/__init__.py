from flask import Flask

app = Flask(__name__, template_folder='templates')
app.secret_key = '123_user_1544'
API_URL = 'http://localhost:8000'


from . import routers, utils 
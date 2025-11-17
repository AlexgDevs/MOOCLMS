from os import getenv
from client import app
from dotenv import load_dotenv

if __name__ == '__main__':
    app.run(port=int(getenv('PORT')), host='0.0.0.0', debug=False)
from flask import (
    make_response, 
    jsonify, flash, 
    redirect, 
    url_for, 
    render_template
)

from .. import app 
from ..utils import AauthClient

@app.get('/')
@AauthClient.auth_required
async def home():
    user = AauthClient.get_current_user()
    return f'hello, {user.get('name')}'
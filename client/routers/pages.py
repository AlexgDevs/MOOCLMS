from flask import make_response, jsonify, flash, redirect, url_for, render_template

from .. import app 


@app.get('/home')
async def home():
    return 'hello'
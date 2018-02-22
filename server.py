from flask import Flask, current_app, request, jsonify, Response, redirect,send_from_directory
from crawler import *

app = Flask(__name__)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/capturar', methods=['GET', 'POST'])
def capturar():
    url = request.form['url']
    file_name = iniciar(url)
    return send_from_directory(directory=current_app.root_path, filename=file_name)

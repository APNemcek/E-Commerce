import os
from flask import Flask, request, render_template, redirect, url_for
from conexion import connectionBD

app = Flask(__name__)
app.secret_key = 'Clave?' 
app_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(app_dir, 'templates')
static_folder = os.path.join(template_folder, 'static')
app.template_folder = template_folder
app.static_folder = static_folder
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


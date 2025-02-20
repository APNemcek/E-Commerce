import os
from flask import Flask, session
from route import route
from controller import app
 
def main():
    
    app.config['SECRET_KEY'] = 'Clave?'

    route(app)
    
    app.run('0.0.0.0', 5000, debug=True) 
    
main()
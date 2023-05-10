import os
from flask import session

from config.config import flask_cfg

secret_key = os.urandom(64)

def apply_sessions(app):
    '''
    Aplica a una aplicación de Flask la capacidad de tener sesiones
    '''
    app.secret_key = secret_key

def get_secret_key(app):
    '''
    Obtiene la secret key en uso
    '''
    return app.secret_key

def check_session(session_login, new, fields=flask_cfg["session"]["min_requirements"], new_user=flask_cfg["session"]["new_requirements"]):
    '''
    Comprueba si la sesión tiene los campos necesarios
    params:
    
    session_login => diccionario con los datos de la sesión entrante
    new => booleano para verificar que la sesión es nueva
    fields => campos mínimos necesarios para poder iniciar sesión
    new_user => campos necesarios en caso de ser una sesión nueva
    '''
    # nos aseguramos que es un diccionario
    if type(session_login) != dict:
        return False
    
    # si se indica que es un nuevo usuario se añaden los campos necesarios
    if new:
        fields += new_user
    
    # recorremos los campos necesarios para comprobar que existen en los datos de sesion
    for key in fields:
        if key not in session_login:
            return False
    
    return True

def init_session(session_obj, data, fields=flask_cfg["session"]["min_requirements"]+flask_cfg["session"]["new_requirements"], permanent=False):
    '''
    Inicia la sesion con los datos necesarios
    params:
    
    session_obj => objeto sesion de Flask
    data => información de la sesión para iniciar
    '''
    # comprobamos que la información para iniciar sesion es un diccionario
    if type(data) != dict:
        return False 
    
    # definimos la permanencia de la sesión
    session_obj.permanent = permanent
    
    # inicializamos los datos de sesión
    for key in fields:
        try:
            session_obj[key] = data[key]
        except:
            return None
    
    return session_obj

__all__ = ["apply_sessions", "get_secret_key", "check_session", "init_session"]
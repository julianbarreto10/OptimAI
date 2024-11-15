from flask import Blueprint, render_template, request, flash
from app.data_request import driver_request, router_request, bi_request
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('base.html')

@bp.route('/drivers', methods=['GET', 'POST'])
def drivers():
    if request.method == 'POST':
        data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "tp_veh": request.form.get('tp_veh'),
            "capacity": request.form.get('capacity'),
            "client_id": request.form.get('client_id'),
        }
        message=driver_request(data)
        flash(message)
        print(data)  # Aquí podrías procesar la información
    return render_template('drivers.html')

@bp.route('/enrutador', methods=['GET', 'POST'])
def enrutador():
    if request.method == 'POST':
        data = json.loads(str(request.form.get('info_enrutamiento')))
        message=router_request(data)
        flash(message)
        print(data)  # Aquí podrías procesar la información
    return render_template('enrutador.html')

@bp.route('/modulo_bi', methods=['GET', 'POST'])
def modulo_bi():
    if request.method == 'POST':
        data = {"client_id": request.form.get('client')}
        message=bi_request(data)
        flash(message)
        print(data)  # Aquí podrías procesar la información
    return render_template('modulo_bi.html')

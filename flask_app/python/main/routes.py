from flask import current_app, Blueprint, json, render_template, send_file, jsonify, request
from flask_app import db
from flask_app.python.models import Cars

from datetime import datetime
import csv

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Locadora de veículos')

### CADASTRO DE VEICULOS ###
@main.route('/car-register', methods=['POST'])
def car_register():
	'''
	Rota para cadastro dos veículos no banco de dados
	'''
	data = request.get_json()
	if data:
		for x in data.keys():
			if x!='estado':
				if data[x]=="" or data[x]==None or len(data[x])==0:
					return(jsonify(status="Error", msg="Preencha todos os campos"))
		
		if db.session.query(Cars).filter_by(placa=data['placa']).first():
			return(jsonify(status="Error", msg="Placa já existe"))
		
		elif len(data['placa'])!=7:
			return(jsonify(status="Error", msg="Placa inválida"))
	
		else:
			car = Cars(
				modelo = data['modelo'],
				placa = data['placa'],
				ano = data['ano'],
				estado = data['estado'],
			)
			db.session.add(car)
			db.session.commit()
			return(jsonify(status="Success", msg="Veículo registrado com sucesso", dados=car.serialize))

	else:
		return(jsonify(status="Error", msg="Nenhum dado recebido"))

@main.route('/cars-get', methods=['GET'])
def cars_get():
	cars = Cars.query.all()
	list_of_cars = []
	for car in cars:
		print(car.serialize)
		list_of_cars.append(car.serialize)
	return(jsonify(status="Success", msg="Lista de carros registrados", cars=list_of_cars))

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
				alugado = False,
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
		c = car.serialize
		if c['estado'] == True:
			c['estado'] = "Liberado"
		else:
			c['estado'] = "Manutenção"
		if c['alugado'] == True:
			c['alugado'] = "Veículo reservado"
			c['termino_aluguel'] = c['termino_aluguel'].strftime("%d/%m/%Y")
			c['inicio_aluguel'] = c['inicio_aluguel'].strftime("%d/%m/%Y")
		else:
			c['alugado'] = "Veículo sem reserva"		
			c['termino_aluguel'] = "-"		
			c['inicio_aluguel'] = "-"		
		list_of_cars.append(c)
	return(jsonify(status="Success", msg="Lista de carros registrados", cars=list_of_cars))

@main.route('/reservar', methods=['POST'])
def reservar():
	'''
	Adicionar reserva veículos no banco de dados
	'''
	data = request.get_json()
	car = db.session.query(Cars).filter_by(id=data['id']).first()
	car.alugado = True
	car.termino_aluguel = datetime.strptime(data['termino'], '%Y-%m-%d')
	car.inicio_aluguel = datetime.strptime(data['inicio'], '%Y-%m-%d')
	db.session.commit()

	print(data['termino'], data['inicio'])
	
	return(jsonify(status="Success", msg="Reserva salva", cars=data))

@main.route('/cancelar-reserva', methods=['POST'])
def cancelar_reserva():
	'''
	Cancelar reserva veículos no banco de dados
	'''
	data = request.get_json()
	car = db.session.query(Cars).filter_by(id=data['id']).first()
	print(car.serialize)
	car.alugado = False
	db.session.commit()
	
	return(jsonify(status="Success", msg="Reserva cancelada", cars=data))


from flask import current_app, Blueprint, json, render_template, send_file, jsonify, request
from flask_app import db
from flask_app.python.models import Cars
#from flask_app.python.main.utils import update_last_status, humidifier

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
# 	size = 60
# 	if len(data)<size:
# 		size = len(data)
# 	temps=[]
# 	hums=[]
# 	times=[]
# 	states=[]
# 	for i in range(-size, 0):
# 		temps.append(data[i].serialize["temperature"])
# 		hums.append(data[i].serialize["humidity"])
# 		times.append(data[i].serialize["time"])
# 		states.append(data[i].serialize["humidifier_state"])

# 	data = {
# 		"temperature": temps,
# 		"humidity": hums,
# 		"time": times,
# 		"humidifier_state": states,
# 	}

# 	return(data)

# @main.route('/get-csv-db', methods=['GET'])
# def get_csv_db():
# 	data = Data.query.all()
# 	header = ["timestamp", "temperatura", "umidade", "estado_do_umidificador"]
# 	rows = []
# 	for d in data:
# 		rows.append([
# 			d.serialize["time"],
# 			d.serialize["temperature"], 
# 			d.serialize["humidity"], 
# 			d.serialize["humidifier_state"]
# 		])

# 	path = 'banco_de_dados.csv'
# 	with open(f"flask_app/{path}", 'w', encoding='UTF8') as f:
# 		writer = csv.writer(f)
# 		writer.writerow(header)
# 		writer.writerows(rows)
		
# 	return send_file(path, as_attachment=True)

# @main.route('/get-last-status', methods=['GET'])
# def get_last_status():
# 	last = db.session.query(LastStatus).get(1).serialize
# 	last["auto_control"] = current_app.config["auto_control_humidity"]
# 	return(last)

# @main.route('/get-set-point', methods=['GET'])
# def get_set_point():
#     set_point = db.session.query(SetPoint).get(1)
#     return(set_point.serialize)

# @main.route('/post-update-info', methods=['POST'])
# def post_update_info():
# 	data = request.get_json()

# 	set_point = db.session.query(SetPoint).get(1)
# 	if set_point:
# 		set_point.humidity_set_point = data['humidity_set_point']
# 		set_point.humidity_deviation = data['humidity_deviation']
# 	else:
# 		set_point = SetPoint(
# 				humidity_set_point = data['humidity_set_point'],
# 				humidity_deviation = data['humidity_deviation'],
# 			)
# 		db.session.add(set_point)
# 	db.session.commit()
# 	return(data)

# @main.route('/post-update-auto-control', methods=['POST'])
# def post_update_auto_control():
# 	data = request.get_json()
# 	current_app.config["auto_control_humidity"] = data['auto_control']
# 	print(current_app.config["auto_control_humidity"])
# 	return({'auto_control': current_app.config["auto_control_humidity"]})

# @main.route('/post-humi-on-off', methods=['POST'])
# def post_humi_on_off():
# 	data = request.get_json()
	
# 	last = get_last_status()
# 	if last['humidifier_state'] == 1:
# 		humidifier(0)
# 		update_last_status(last['humidity'], last['temperature'])
# 		return({'humi_state': False})
# 	else:
# 		humidifier(1)
# 		update_last_status(last['humidity'], last['temperature'])
# 		return({'humi_state': True})

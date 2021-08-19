from flask import current_app

from flask_app import db
from flask_app.python.models import Cars

from datetime import datetime

# def save_to_db(self, humidity, temperature):
#     humidity = round(self.humidity_mean/self.counter, 1)
#     print(f'Saving Data to DB: {datetime.now()}, State: {current_app.config["humidifier_state"] }, {humidity}%,  {temperature}°C')
#     data = Data(
#         temperature = temperature,
#         humidity = humidity,
#         humidifier_state = current_app.config["humidifier_state"],
#         time = datetime.now(),
#     )
#     db.session.add(data)
#     db.session.commit()
#     self.humidity_mean = 0
#     self.counter = 0

# def update_last_status(humidity, temperature):    
#     last = db.session.query(LastStatus).get(1)
#     if last:
#         last.humidity = humidity
#         last.temperature = temperature
#         last.humidifier_state = current_app.config["humidifier_state"] 
#     else:
#         last = LastStatus(
#             humidity = humidity,
#             temperature = temperature,
#             humidifier_state = current_app.config["humidifier_state"] 
#         )
#         db.session.add(last)
#     db.session.commit()

# def get_last_status():
#     last = db.session.query(LastStatus).get(1)
#     return(last.serialize)

# def get_set_point():
#     set_point = db.session.query(SetPoint).get(1)
#     return(set_point.serialize)

# def get_humidity_temperature(pin_number = 2, DHT_SENSOR = Adafruit_DHT.DHT22):
#     humidity, temperature = None, None
#     while humidity == None or temperature == None:
#         humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin_number)

#         if humidity == None or temperature == None:
#             #print("Error, none, none")
#             pass
#         else:
#             humidity, temperature = round(humidity, 2), round(temperature, 2)

#             if 0<=humidity<=99.9:
#                 return(humidity, temperature)
#             else:
#                 #print("Error, humidity")
#                 humidity, temperature = None, None
#         time.sleep(1)
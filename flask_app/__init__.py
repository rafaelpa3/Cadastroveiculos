from flask import Flask
from flask_sqlalchemy import SQLAlchemy

####### RESTART DB? #######
RESTART_DB = False
###########################

db = SQLAlchemy()

def create_app(config_class):
    app = Flask(__name__)

    print(f"STARTING CONFIG MODE: {config_class.MODE}")
    app.config.from_object(config_class)
    
    db.init_app(app)

    from flask_app.python.main.routes import main
    app.register_blueprint(main)

    print("\nRestart DB set to:", RESTART_DB, '\n')
    
    from flask_app.python.models import Cars
    if RESTART_DB is True:
        with app.app_context():
            print("Dropando tabelas")
            db.drop_all()
            print("Criando tabelas")
            db.create_all()
            ## DEFAULT PRA TEST ##
            car1 = Cars(
        		modelo = "HB20",
        		placa = "AAA1A11",
        		ano = 2019,
            	estado = True,
 			)
            car2 = Cars(
        		modelo = "Palio",
        		placa = "BBB2B22",
        		ano = 2012,
            	estado = False,
 			)
            db.session.add(car1)
            db.session.add(car2)
            db.session.commit()
            print("Banco de dados restaurado. \n")

    return app

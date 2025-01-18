from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/nameDataBase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели базы данных
class Airplane(db.Model):
    __tablename__ = 'airplane'
    airplane_id = db.Column(db.String, primary_key=True)
    airplane_type = db.Column(db.String, nullable=False)
    airplane_speed = db.Column(db.Integer, nullable=False)
    airplane_hight = db.Column(db.Integer, nullable=False)
    airplane_capacity = db.Column(db.Integer, nullable=False)

class Client(db.Model):
    __tablename__ = 'client'
    client_passport_id = db.Column(db.String, primary_key=True)
    client_name = db.Column(db.String, nullable=False)
    client_surname = db.Column(db.String, nullable=False)
    client_patronymic = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)

class Flight(db.Model):
    __tablename__ = 'flight'
    flight_name = db.Column(db.String, primary_key=True)
    flight_departure = db.Column(db.String, nullable=False)
    flight_arrival = db.Column(db.String, nullable=False)
    timestamp_departure = db.Column(db.DateTime, nullable=False)
    timestamp_arrival = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    fk_airplane_id = db.Column(db.String, db.ForeignKey('airplane.airplane_id'), nullable=False)

class ClientFlight(db.Model):
    __tablename__ = 'client_flight'
    client_passport_id = db.Column(db.String, db.ForeignKey('client.client_passport_id'), primary_key=True, nullable=False)
    flight_name = db.Column(db.String, db.ForeignKey('flight.flight_name'), primary_key=True, nullable=False)
    ticket_number = db.Column(db.String, unique=True, nullable=False)

# Интерфейс для работы с таблицей Airplane
@app.route('/')
def index():
    airplanes = Airplane.query.all()
    clients = Client.query.all()
    flights = Flight.query.all()
    client_flights = ClientFlight.query.all()
    return render_template('index.html', airplanes=airplanes, clients=clients, flights=flights, client_flights=client_flights)

# CRUD операции для Airplane
@app.route('/airplanes', methods=['POST'])
def create_airplane():
    data = request.form
    new_airplane = Airplane(
        airplane_id=data['airplane_id'],
        airplane_type=data['airplane_type'],
        airplane_speed=data['airplane_speed'],
        airplane_hight=data['airplane_hight'],
        airplane_capacity=data['airplane_capacity']
    )
    db.session.add(new_airplane)
    db.session.commit()
    return index()

@app.route('/airplanes/<airplane_id>/update', methods=['POST'])
def update_airplane(airplane_id):
    data = request.form
    airplane = Airplane.query.get(airplane_id)
    if airplane:
        airplane.airplane_type = data['airplane_type']
        airplane.airplane_speed = data['airplane_speed']
        airplane.airplane_hight = data['airplane_hight']
        airplane.airplane_capacity = data['airplane_capacity']
        db.session.commit()
    return index()

@app.route('/airplanes/<airplane_id>/delete', methods=['POST'])
def delete_airplane(airplane_id):
    airplane = Airplane.query.get(airplane_id)
    if airplane:
        db.session.delete(airplane)
        db.session.commit()
    return index()

# CRUD операции для Client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.form
    new_client = Client(
        client_passport_id=data['client_passport_id'],
        client_name=data['client_name'],
        client_surname=data['client_surname'],
        client_patronymic=data['client_patronymic'],
        password_hash=data['password_hash'],
        salt=data['salt']
    )
    db.session.add(new_client)
    db.session.commit()
    return index()

@app.route('/clients/<client_passport_id>/update', methods=['POST'])
def update_client(client_passport_id):
    data = request.form
    client = Client.query.get(client_passport_id)
    if client:
        client.client_name = data['client_name']
        client.client_surname = data['client_surname']
        client.client_patronymic = data['client_patronymic']
        client.password_hash = data['password_hash']
        client.salt = data['salt']
        db.session.commit()
    return index()

@app.route('/clients/<client_passport_id>/delete', methods=['POST'])
def delete_client(client_passport_id):
    client = Client.query.get(client_passport_id)
    if client:
        db.session.delete(client)
        db.session.commit()
    return index()

# CRUD операции для Flight
@app.route('/flights', methods=['POST'])
def create_flight():
    data = request.form
    new_flight = Flight(
        flight_name=data['flight_name'],
        flight_departure=data['flight_departure'],
        flight_arrival=data['flight_arrival'],
        timestamp_departure=data['timestamp_departure'],
        timestamp_arrival=data['timestamp_arrival'],
        ticket_price=data['ticket_price'],
        fk_airplane_id=data['fk_airplane_id']
    )
    db.session.add(new_flight)
    db.session.commit()
    return index()

@app.route('/flights/<flight_name>/update', methods=['POST'])
def update_flight(flight_name):
    data = request.form
    flight = Flight.query.get(flight_name)
    if flight:
        flight.flight_departure = data['flight_departure']
        flight.flight_arrival = data['flight_arrival']
        flight.timestamp_departure = data['timestamp_departure']
        flight.timestamp_arrival = data['timestamp_arrival']
        flight.ticket_price = data['ticket_price']
        flight.fk_airplane_id = data['fk_airplane_id']
        db.session.commit()
    return index()

@app.route('/flights/<flight_name>/delete', methods=['POST'])
def delete_flight(flight_name):
    flight = Flight.query.get(flight_name)
    if flight:
        db.session.delete(flight)
        db.session.commit()
    return index()

# CRUD операции для ClientFlight
@app.route('/client_flights', methods=['POST'])
def create_client_flight():
    data = request.form
    new_client_flight = ClientFlight(
        client_passport_id=data['client_passport_id'],
        flight_name=data['flight_name'],
        ticket_number=data['ticket_number']
    )
    db.session.add(new_client_flight)
    db.session.commit()
    return index()

@app.route('/client_flights/<int:id>/delete', methods=['POST'])
def delete_client_flight(id):
    client_flight = ClientFlight.query.get(id)
    if client_flight:
        db.session.delete(client_flight)
        db.session.commit()
    return index()

# Запуск приложения
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

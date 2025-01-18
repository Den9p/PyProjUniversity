from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)

# Настройки подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
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

class Flight(db.Model):  # Убедитесь, что этот класс объявлен и импортирован
    __tablename__ = 'flight'
    flight_name = db.Column(db.String, primary_key=True)
    flight_departure = db.Column(db.String, nullable=False)
    flight_arrival = db.Column(db.String, nullable=False)
    timestamp_departure = db.Column(db.DateTime, nullable=False)
    timestamp_arrival = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    fk_airplane_id = db.Column(db.String, db.ForeignKey('airplane.airplane_id', ondelete='CASCADE'), nullable=False)

class ClientFlight(db.Model):
    __tablename__ = 'client_flight'
    client_passport_id = db.Column(db.String, db.ForeignKey('client.client_passport_id'), primary_key=True, nullable=False)
    flight_name = db.Column(db.String, db.ForeignKey('flight.flight_name'), primary_key=True, nullable=False)
    ticket_number = db.Column(db.String, unique=True, nullable=False)

# CRUD операции для Airplane
@app.route('/airplanes', methods=['GET'])
def get_airplanes():
    airplanes = Airplane.query.all()
    return jsonify([{
        'airplane_id': a.airplane_id,
        'airplane_type': a.airplane_type,
        'airplane_speed': a.airplane_speed,
        'airplane_hight': a.airplane_hight,
        'airplane_capacity': a.airplane_capacity
    } for a in airplanes])

@app.route('/airplanes', methods=['POST'])
def create_airplane():
    data = request.json
    new_airplane = Airplane(
        airplane_id=data['airplane_id'],
        airplane_type=data['airplane_type'],
        airplane_speed=data['airplane_speed'],
        airplane_hight=data['airplane_hight'],
        airplane_capacity=data['airplane_capacity']
    )
    db.session.add(new_airplane)
    db.session.commit()
    return jsonify({'message': 'Airplane created successfully'}), 201

@app.route('/airplanes/<airplane_id>', methods=['GET'])
def get_airplane(airplane_id):
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404
    return jsonify({
        'airplane_id': airplane.airplane_id,
        'airplane_type': airplane.airplane_type,
        'airplane_speed': airplane.airplane_speed,
        'airplane_hight': airplane.airplane_hight,
        'airplane_capacity': airplane.airplane_capacity
    })

@app.route('/airplanes/<airplane_id>', methods=['PUT'])
def update_airplane(airplane_id):
    data = request.json
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404

    airplane.airplane_type = data['airplane_type']
    airplane.airplane_speed = data['airplane_speed']
    airplane.airplane_hight = data['airplane_hight']
    airplane.airplane_capacity = data['airplane_capacity']
    db.session.commit()
    return jsonify({'message': 'Airplane updated successfully'})


@app.route('/airplanes/<airplane_id>', methods=['DELETE'])
def delete_airplane(airplane_id):
    # Сначала удаляем все записи в client_flight, связанные с рейсами, использующими этот самолет
    flights_to_delete = Flight.query.filter_by(fk_airplane_id=airplane_id).all()
    for flight in flights_to_delete:
        # Удаляем все записи из client_flight, которые ссылаются на этот рейс
        client_flights_to_delete = ClientFlight.query.filter_by(flight_name=flight.flight_name).all()
        for client_flight in client_flights_to_delete:
            db.session.delete(client_flight)

        # После этого удаляем сам рейс
        db.session.delete(flight)

    # Теперь можно удалить сам самолет
    airplane = Airplane.query.get(airplane_id)
    if not airplane:
        return jsonify({'message': 'Airplane not found'}), 404

    db.session.delete(airplane)
    db.session.commit()

    return jsonify({'message': 'Airplane and all related flights and client_flight records deleted successfully'})


# Рендеринг главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Запуск приложения
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

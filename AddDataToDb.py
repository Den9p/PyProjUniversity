import psycopg2
from faker import Faker
import random
from datetime import timedelta

# Подключение к базе данных
connection = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Создание объекта Faker
fake = Faker()

# Список данных для airplane_type
airplane_data = [
    {"type": "Airbus A220-100", "speed": 871, "hight": 12500, "capacity": 135},
    {"type": "Airbus A220-300", "speed": 871, "hight": 12500, "capacity": 160},
    {"type": "Airbus A318", "speed": 828, "hight": 12500, "capacity": 132},
    {"type": "Airbus A319", "speed": 828, "hight": 12500, "capacity": 160},
    {"type": "Airbus A320", "speed": 828, "hight": 12500, "capacity": 180},
    {"type": "Airbus A321", "speed": 828, "hight": 12500, "capacity": 220},
    {"type": "Airbus A330-200", "speed": 913, "hight": 12500, "capacity": 406},
    {"type": "Airbus A330-300", "speed": 913, "hight": 12500, "capacity": 440},
    {"type": "Airbus A340-300", "speed": 871, "hight": 12500, "capacity": 440},
    {"type": "Airbus A350-900", "speed": 945, "hight": 13100, "capacity": 440},
    {"type": "Airbus A350-1000", "speed": 945, "hight": 13100, "capacity": 480},
    {"type": "Airbus A380-800", "speed": 945, "hight": 13100, "capacity": 853},
    {"type": "Antonov An-148", "speed": 800, "hight": 12200, "capacity": 80},
    {"type": "Antonov An-158", "speed": 870, "hight": 12200, "capacity": 99},
    {"type": "Antonov An-178", "speed": 825, "hight": 12200, "capacity": 99},
    {"type": "Boeing 717", "speed": 896, "hight": 12500, "capacity": 134},
    {"type": "Boeing 737-300", "speed": 876, "hight": 12500, "capacity": 149},
    {"type": "Boeing 737-400", "speed": 876, "hight": 12500, "capacity": 168},
    {"type": "Boeing 737-500", "speed": 876, "hight": 12500, "capacity": 132},
    {"type": "Boeing 737-600", "speed": 876, "hight": 12500, "capacity": 130},
    {"type": "Boeing 737-700", "speed": 876, "hight": 12500, "capacity": 149},
    {"type": "Boeing 737-800", "speed": 876, "hight": 12500, "capacity": 189},
    {"type": "Boeing 737-900ER", "speed": 876, "hight": 12500, "capacity": 220},
    {"type": "Boeing 737 MAX 7", "speed": 834, "hight": 12500, "capacity": 172},
    {"type": "Boeing 737 MAX 8", "speed": 834, "hight": 12500, "capacity": 210},
    {"type": "Boeing 737 MAX 9", "speed": 834, "hight": 12500, "capacity": 220},
    {"type": "Boeing 737 MAX 10", "speed": 834, "hight": 12500, "capacity": 230},
    {"type": "Boeing 747-400", "speed": 913, "hight": 13100, "capacity": 660},
    {"type": "Boeing 747-8", "speed": 913, "hight": 13100, "capacity": 605}
]

# Заполнение таблицы airplane
for _ in range(100):
    airplane_id = fake.unique.bothify(text="???##")
    airplane = random.choice(airplane_data)
    cursor.execute(
        """
        INSERT INTO airplane (airplane_id, airplane_type, airplane_speed, airplane_hight, airplane_capacity)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (airplane_id, airplane["type"], airplane["speed"], airplane["hight"], airplane["capacity"])
    )

# Заполнение таблицы client
for _ in range(100):
    client_passport_id = fake.unique.bothify(text="????######")
    client_name = fake.first_name()
    client_surname = fake.last_name()
    client_patronymic = fake.first_name() if random.choice([True, False]) else None
    password_hash = fake.sha256()
    salt = fake.sha256()

    cursor.execute(
        """
        INSERT INTO client (client_passport_id, client_name, client_surname, client_patronymic, password_hash, salt)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (client_passport_id, client_name, client_surname, client_patronymic, password_hash, salt)
    )

# Заполнение таблицы flight
cursor.execute("SELECT airplane_id FROM airplane")
airplane_ids = [row[0] for row in cursor.fetchall()]
if not airplane_ids:
    raise ValueError("No airplane IDs found in the airplane table. Ensure that the table is populated before this step.")

for _ in range(100):
    flight_name = fake.unique.bothify(text="FL###")
    flight_departure = fake.city()
    flight_arrival = fake.city()
    while flight_arrival == flight_departure:
        flight_arrival = fake.city()
    timestamp_departure = fake.date_time_this_year()
    timestamp_arrival = timestamp_departure + timedelta(hours=random.randint(1, 12))
    ticket_price = random.randint(50, 500)
    fk_airplane_id = random.choice(airplane_ids)

    cursor.execute(
        """
        INSERT INTO flight (flight_name, flight_departure, flight_arrival, timestamp_departure, timestamp_arrival, ticket_price, fk_airplane_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (flight_name, flight_departure, flight_arrival, timestamp_departure, timestamp_arrival, ticket_price, fk_airplane_id)
    )

# Заполнение таблицы client_flight
cursor.execute("SELECT client_passport_id FROM client")
client_passport_ids = [row[0] for row in cursor.fetchall()]
if not client_passport_ids:
    raise ValueError("No client passport IDs found in the client table.")

cursor.execute("SELECT flight_name FROM flight")
flight_names = [row[0] for row in cursor.fetchall()]
if not flight_names:
    raise ValueError("No flight names found in the flight table.")

for _ in range(100):
    client_passport_id = random.choice(client_passport_ids)
    flight_name = random.choice(flight_names)
    ticket_number = fake.unique.bothify(text="##########??")

    cursor.execute(
        """
        INSERT INTO client_flight (client_passport_id, flight_name, ticket_number)
        VALUES (%s, %s, %s)
        """,
        (client_passport_id, flight_name, ticket_number)
    )

# Сохранение изменений и закрытие соединения
connection.commit()
cursor.close()
connection.close()

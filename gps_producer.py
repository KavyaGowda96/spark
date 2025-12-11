import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# List of fake vehicle IDs
VEHICLE_IDS = ["CAR_001", "CAR_002", "CAR_003", "TRUCK_01", "BUS_10"]

# Some base location (e.g., Bangalore)
BASE_LAT = 12.9716
BASE_LON = 77.5946

def generate_vehicle_data():
    vehicle_id = random.choice(VEHICLE_IDS)

    # Random small movement around base location
    lat = BASE_LAT + random.uniform(-0.05, 0.05)
    lon = BASE_LON + random.uniform(-0.05, 0.05)

    # Random speed between 0 and 120 km/h
    speed = round(random.uniform(0, 120), 2)

    # Current time as ISO string
    ts = datetime.utcnow().isoformat()

    return {
        "vehicle_id": vehicle_id,
        "latitude": lat,
        "longitude": lon,
        "speed": speed,
        "event_time": ts
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092"
    )

    topic = "vehicle_gps"

    print("🚚 Sending GPS data to Kafka topic:", topic)

    while True:
        data = generate_vehicle_data()
        msg = json.dumps(data).encode("utf-8")

        producer.send(topic, msg)
        producer.flush()

        print("Sent:", data)

        # Wait 1 second between messages
        time.sleep(1)

if __name__ == "__main__":
    main()

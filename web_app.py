from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer
import json
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store latest vehicle data
vehicle_data = {}

def consume_kafka_data():
    """Background thread to consume Kafka messages and emit to web clients"""
    consumer = KafkaConsumer(
        'vehicle_gps',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("🎯 Starting Kafka consumer for web dashboard...")
    
    for message in consumer:
        data = message.value
        vehicle_id = data['vehicle_id']
        
        # Store latest data for each vehicle
        vehicle_data[vehicle_id] = data
        
        # Check for overspeed alert
        is_alert = data['speed'] > 80
        
        # Emit to all connected web clients
        socketio.emit('vehicle_update', {
            'vehicle_id': vehicle_id,
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'speed': data['speed'],
            'event_time': data['event_time'],
            'is_alert': is_alert
        })

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/vehicles')
def get_vehicles():
    """API endpoint to get current vehicle data"""
    return json.dumps(vehicle_data)

if __name__ == '__main__':
    # Start Kafka consumer in background thread
    kafka_thread = threading.Thread(target=consume_kafka_data, daemon=True)
    kafka_thread.start()
    
    # Start Flask web server
    print("🚀 Starting web dashboard on http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

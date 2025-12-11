from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import threading
import time
import random
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store latest vehicle data
vehicle_data = {}

# List of fake vehicle IDs
VEHICLE_IDS = ["CAR_001", "CAR_002", "CAR_003", "TRUCK_01", "BUS_10"]

# Base location (Bangalore)
BASE_LAT = 12.9716
BASE_LON = 77.5946

def generate_vehicle_data():
    """Generate simulated GPS data"""
    vehicle_id = random.choice(VEHICLE_IDS)
    
    # Random small movement around base location
    lat = BASE_LAT + random.uniform(-0.05, 0.05)
    lon = BASE_LON + random.uniform(-0.05, 0.05)
    
    # Random speed between 0 and 120 km/h
    speed = round(random.uniform(0, 120), 2)
    
    # Current time as ISO string
    ts = datetime.now().isoformat()
    
    return {
        "vehicle_id": vehicle_id,
        "latitude": lat,
        "longitude": lon,
        "speed": speed,
        "event_time": ts
    }

def simulate_gps_data():
    """Background thread to simulate GPS data and emit to web clients"""
    print("🎯 Starting GPS data simulator...")
    
    while True:
        data = generate_vehicle_data()
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
        
        print(f"📡 Sent: {vehicle_id} - Speed: {data['speed']:.1f} km/h")
        
        # Wait 1 second between updates
        time.sleep(1)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/vehicles')
def get_vehicles():
    """API endpoint to get current vehicle data"""
    return json.dumps(vehicle_data)

if __name__ == '__main__':
    # Start GPS simulator in background thread
    simulator_thread = threading.Thread(target=simulate_gps_data, daemon=True)
    simulator_thread.start()
    
    # Start Flask web server
    print("🚀 Starting web dashboard on http://localhost:5000")
    print("📍 Open your browser and visit: http://localhost:5000")
    socketio.run(app, debug=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

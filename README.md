# GPS Vehicle Tracking System with Web Dashboard

A real-time vehicle tracking system using Apache Spark Streaming, Kafka, and a web-based dashboard.

## Features

- 🚗 Real-time GPS vehicle tracking
- 📍 Interactive map visualization using Leaflet
- ⚠️ Overspeed alerts (>80 km/h)
- 📊 Live statistics dashboard
- 🔄 WebSocket-based real-time updates

## System Architecture

1. **GPS Producer** (`gps_producer.py`) - Simulates GPS data and sends to Kafka
2. **Spark Stream Processor** (`vehicle_tracking_spark.py`) - Processes GPS streams using Apache Spark
3. **Web Dashboard** (`web_app.py`) - Flask-based real-time web interface

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install and start Kafka:
   - Download Kafka from https://kafka.apache.org/downloads
   - Start Zookeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`
   - Start Kafka: `bin/kafka-server-start.sh config/server.properties`

## Usage

### Run the complete system:

1. **Start GPS Producer** (Terminal 1):
```bash
python gps_producer.py
```

2. **Start Web Dashboard** (Terminal 2):
```bash
python web_app.py
```

3. **Open Dashboard** in browser:
```
http://localhost:5000
```

4. **(Optional) Run Spark Processing** (Terminal 3):
```bash
python vehicle_tracking_spark.py
```

## Dashboard Features

- **Live Map**: Shows real-time vehicle positions with color-coded markers
  - Green: Normal speed
  - Red: Overspeed alert
  
- **Vehicle Status**: Lists all active vehicles with current speed and location

- **Statistics**: 
  - Total active vehicles
  - Number of overspeed alerts
  - Average fleet speed

- **Alert History**: Recent overspeed violations

## Configuration

- **Kafka Server**: `localhost:9092`
- **Kafka Topic**: `vehicle_gps`
- **Web Server**: `http://localhost:5000`
- **Overspeed Threshold**: 80 km/h
- **Base Location**: Bangalore (12.9716°N, 77.5946°E)

## Vehicle Data Format

```json
{
  "vehicle_id": "CAR_001",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "speed": 65.5,
  "event_time": "2025-12-11T12:00:00"
}
```

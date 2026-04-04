# GPS Vehicle Tracking System

A real-time GPS vehicle tracking system built with Python (Flask, Apache Kafka, Spark Streaming) and a live web dashboard with interactive map and speed tracking graph.

## Live Dashboard

The web dashboard is deployed on Netlify and features:

- **Interactive Map** - Real-time vehicle positions on a Leaflet map centered on Bangalore, with color-coded markers (green = normal, red = overspeed) and movement trails
- **Speed Tracking Graph** - Full-width Chart.js line graph tracking speed of all 5 vehicles in real-time, with a dashed red speed limit line at 80 km/h
- **Dashboard Stats** - Active vehicle count, average fleet speed, max speed, and total overspeed alerts
- **Vehicle Status Panel** - Live list of all tracked vehicles with current speed and GPS coordinates
- **Overspeed Alerts** - Scrolling alert bar capturing every speed limit violation with vehicle ID, speed, timestamp, and location

## System Architecture

```
GPS Producer (Python)          Spark Stream Processor (Python)
      |                                |
      v                                v
  Apache Kafka  <---->  vehicle_gps topic
      |
      v
Flask Web App (Python) ---> WebSocket ---> Browser Dashboard
```

### Components

| File | Description |
|------|-------------|
| `gps_producer.py` | Simulates GPS data for 5 vehicles and publishes to Kafka topic `vehicle_gps` |
| `vehicle_tracking_spark.py` | Spark Structured Streaming processor - reads from Kafka, computes windowed avg/max speed stats, detects overspeed alerts |
| `web_app.py` | Flask + SocketIO web server that consumes Kafka messages and pushes real-time updates to the browser via WebSocket |
| `web_app_simple.py` | Standalone Flask app with built-in GPS simulator (no Kafka dependency) - good for quick demos |
| `index.html` | Self-contained web dashboard deployed on Netlify with client-side GPS simulation |
| `requirements.txt` | Python dependencies |

## Python Backend Setup

### Prerequisites

- Python 3.8+
- Apache Kafka (for full pipeline)
- Apache Spark (for stream processing)

### Installation

```bash
pip install -r requirements.txt
```

### Quick Start (No Kafka Required)

Run the standalone Flask app with built-in simulation:

```bash
python web_app_simple.py
```

Open http://localhost:5000 in your browser.

### Full Pipeline (With Kafka + Spark)

**Terminal 1** - Start Kafka:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

**Terminal 2** - Start GPS Producer:
```bash
python gps_producer.py
```

**Terminal 3** - Start Web Dashboard:
```bash
python web_app.py
```

**Terminal 4** (Optional) - Start Spark Analytics:
```bash
python vehicle_tracking_spark.py
```

Open http://localhost:5000 in your browser.

## Configuration

| Parameter | Value |
|-----------|-------|
| Kafka Server | `localhost:9092` |
| Kafka Topic | `vehicle_gps` |
| Web Server | `http://localhost:5000` |
| Overspeed Threshold | 80 km/h |
| Base Location | Bangalore (12.9716°N, 77.5946°E) |
| Tracked Vehicles | CAR_001, CAR_002, CAR_003, TRUCK_01, BUS_10 |

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

## Technologies Used

- **Python** - Flask, Flask-SocketIO, kafka-python, PySpark
- **Apache Kafka** - Message streaming
- **Apache Spark** - Stream processing and analytics
- **Leaflet.js** - Interactive maps
- **Chart.js** - Speed tracking graphs
- **HTML/CSS/JavaScript** - Dashboard frontend
- **Netlify** - Static site deployment

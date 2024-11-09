from flask import Flask, request, jsonify
import threading
from attendance_metrics import AttendanceMetrics
from prometheus_client import start_http_server
import time 

app = Flask(__name__)

# Create a global metrics instance
metrics = AttendanceMetrics()
start_http_server(8000)
print("Prometheus metrics server started on port 8000")

@app.route('/attendance', methods=['POST'])
def add_attendance():
    """Add a single attendee"""
    data = request.json
    
    required_fields = ['name', 'workshop_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        metrics.record_attendance(
            name=data['name'],
            workshop_id=data['workshop_id'],
            present=data.get('present', True),
            photo_link=data.get('photo_link')
        )
        return jsonify({'message': 'Attendance recorded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/attendance/bulk', methods=['POST'])
def bulk_attendance():
    """Add multiple attendees"""
    data = request.json
    
    if not isinstance(data, list):
        return jsonify({'error': 'Expected a list of attendees'}), 400
    
    try:
        metrics.bulk_update(data)
        return jsonify({'message': f'Recorded attendance for {len(data)} attendees'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/attendance/<name>/<workshop_id>', methods=['DELETE'])
def remove_attendance(name, workshop_id):
    """Mark an attendee as not present"""
    try:
        metrics.record_attendance(name=name, workshop_id=workshop_id, present=False)
        return jsonify({'message': 'Attendance removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/help', methods=['GET'])
def help():
    """Provide detailed API documentation"""
    help_text = """
    Available Endpoints:
    
    1. POST /attendance - Add a single attendee's attendance
        Request JSON body:
        {
            "name": "John Doe",
            "workshop_id": "workshop123",
            "present": true,  # Optional: Default is true
            "photo_link": "http://example.com/photo.jpg"  # Optional
        }
        
    2. POST /attendance/bulk - Add multiple attendees' attendance
        Request JSON body:
        [
            {
                "name": "John Doe",
                "workshop_id": "workshop123",
                "present": true,
                "photo_link": "http://example.com/photo.jpg"
            },
            {
                "name": "Jane Doe",
                "workshop_id": "workshop124",
                "present": false
            }
        ]
        
    3. DELETE /attendance/<name>/<workshop_id> - Remove an attendee's attendance
        Example: DELETE /attendance/John%20Doe/workshop123

    Prometheus Metrics:
    - /metrics - Exposes metrics for Prometheus to scrape
    """
    return jsonify({'help': help_text}), 200

def run_flask():
    """Run Flask app on a different port than Prometheus"""
    app.run(host='0.0.0.0', port=5000)

def main():
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Flask API server started on port 5000")

    # Keep the main thread running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()


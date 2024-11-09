from prometheus_client import Gauge, start_http_server
from datetime import datetime
import time
import pytz

# Separate gauges for different metrics
attendance_status = Gauge(
    'workshop_attendance_status',
    'Indicates the attendance status of a workshop attendee',
    ['name', 'workshop_id', 'photo']
)

last_seen_time = Gauge(
    'workshop_last_seen_time',
    'Records the last seen timestamp of an attendee',
    ['name', 'workshop_id']
)

arrival_time = Gauge(
    'workshop_arrival_time',
    'Records the arrival time of an attendee',
    ['name', 'workshop_id']
)

class AttendanceMetrics:
    def __init__(self, port=8000):
        start_http_server(port)
        print(f"Prometheus metrics server started on port {port}")
        
    def record_attendance(self, name: str, workshop_id: str, present: bool = True, photo_link: str = None):
        """
        Record attendance using separate gauges for status, last seen, and arrival time
        
        Args:
            name: Name of the attendee
            workshop_id: Unique identifier for the workshop
            present: Whether the attendee is present
            photo_link: URL of the attendee's photo (Optional)
        """
        # Get the current time in Moldova's timezone
        local_timezone = pytz.timezone("Europe/Chisinau")  # Moldova timezone
        current_time = datetime.now(local_timezone)
        
        # Convert the time to Unix timestamp in seconds
        current_time_unix = int(current_time.timestamp() * 1000)  # Unix timestamp in seconds
       
        # Record attendance status
        attendance_status.labels(name=name, workshop_id=workshop_id, photo=photo_link).set(1 if present else 0)
        
        # Record last seen time
        last_seen_time.labels(name=name, workshop_id=workshop_id).set(current_time_unix)
        
        # Record arrival time
        arrival_time.labels(name=name, workshop_id=workshop_id).set(current_time_unix)

    def bulk_update(self, attendees):
        """
        Bulk update attendance for multiple attendees
        """
        for attendee in attendees:
            self.record_attendance(
                name=attendee['name'],
                workshop_id=attendee['workshop_id'],
                present=attendee.get('present', True),
                photo_link=attendee.get('photo_link')  # Add photo link if available
            )

def main():
    metrics = AttendanceMetrics(port=8000)
    
    # Example usage with the photo link
    photo_url = "https://images.inc.com/uploaded_files/image/1024x576/getty_481292845_77896.jpg"
    metrics.record_attendance("John Doe", "WORKSHOP-001", True, photo_link=photo_url)
    
    # Bulk update example with photos for each attendee
    attendees = [
        {"name": "Alice Brown", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Bob Wilson", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Charlie Davis", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "David Smith", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Eva White", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Frank Green", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Grace Harris", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Henry Lee", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Ivy Taylor", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Jack Walker", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Jack Joe", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Mary Sue", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "George Washington", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url},
        {"name": "Mihai Eminescu", "workshop_id": "WORKSHOP-001", "present": True, "photo_link": photo_url}
    ]
    
    metrics.bulk_update(attendees)
    
    # Keep the server running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()


from prometheus_client import Gauge
from datetime import datetime

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
    def __init__(self):
        """
        Initializes the attendance metrics instance
        """
        pass
        
    def record_attendance(self, name: str, workshop_id: str, present: bool = True, photo_link: str = None):
        """
        Record attendance using separate gauges for status, last seen, and arrival time
        """
        current_time = datetime.now()
        current_time_unix = int(current_time.timestamp() * 1000)
        
        attendance_status.labels(name=name, workshop_id=workshop_id, photo=photo_link).set(1 if present else 0)
        last_seen_time.labels(name=name, workshop_id=workshop_id).set(current_time_unix)
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
                photo_link=attendee.get('photo_link')
            )


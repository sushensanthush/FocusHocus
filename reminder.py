# In this file, I have created a Reminder class that will handle the logic for sending notifications at regular intervals. 
# The class uses the plyer library to send notifications and runs in a separate thread to avoid blocking the main program. 
# The start() method begins the notification loop, and the stop() method can be called to end it.
import time
from threading import Thread, Event
from plyer import notification

class Reminder:
    def __init__(self, interval_minutes=60, message="Time to take a break!"):
        self.interval = interval_minutes * 60  # seconds
        self.message = message
        self._stop_event = Event()
        self.thread = None

    def _notify_loop(self):
        # Use wait() instead of sleep() so it can be interrupted immediately
        while not self._stop_event.wait(self.interval):
            # If wait() returns False, it means the timeout hit (time is up)
            # If it returns True, it means the stop button was pressed
            notification.notify(
                title="Screen Time Reminder",
                message=self.message,
                app_name="ZonedIn",
                timeout=10
            )

    def start(self):
        if self.thread and self.thread.is_alive():
            return 
        self._stop_event.clear()
        self.thread = Thread(target=self._notify_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_event.set() # Wakes up the .wait() immediately
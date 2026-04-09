# main.py
import sys
from gui import ReminderApp

if __name__ == "__main__":
    app = ReminderApp()
    
    # Handle the "X" button click properly
    app.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    
    try:
        app.mainloop()
    except (KeyboardInterrupt, SystemExit):
        # Exit cleanly without errors
        pass
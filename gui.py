import customtkinter as ctk
from reminder import Reminder
from config import INTERVAL_MINUTES, MESSAGE
import threading, time, os
from PIL import Image

# Its Global settings for the app, including appearance mode and color theme.
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# My color palette for the app, including hover states and disabled states for buttons
GOLD = "#FFD700"
GOLD_HOVER = "#E6C200"
SUCCESS_GREEN = "#28a745"
SUCCESS_HOVER = "#218838"
DANGER_RED = "#dc3545"
DANGER_HOVER = "#c82333"
DISABLED_GREY = "#D1D1D1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUN_ICON = os.path.join(BASE_DIR, "sun.png")
MOON_ICON = os.path.join(BASE_DIR, "moon.png")

sun_img = Image.open(SUN_ICON).resize((24, 24))
moon_img = Image.open(MOON_ICON).resize((24, 24))

class ReminderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Screen Time Reminder")
        self.geometry("450x480")
        self.resizable(False, False)

        # I used Header frame to hold the app title and the theme toggle button, giving it a clean and organized look.
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 10), padx=30)

        self.header = ctk.CTkLabel(header_frame, text="Focus Hocus",
                                   font=ctk.CTkFont(family="Inter", size=22, weight="bold"))
        self.header.pack(side="left")

        # UI of Dark and light theme toggle button
        self.theme_icon = ctk.CTkImage(light_image=sun_img, dark_image=moon_img, size=(22,22))
        self.theme_button = ctk.CTkButton(
            header_frame, image=self.theme_icon, text="",
            width=45, height=45, fg_color=GOLD, hover_color=GOLD_HOVER,
            corner_radius=12, command=self.toggle_theme
        )
        self.theme_button.pack(side="right")

        # In here I have created input fields for the user to set the reminder interval and message.
        self.interval_label = ctk.CTkLabel(self, text="Interval (minutes)", font=ctk.CTkFont(size=13, weight="bold"))
        self.interval_label.pack(pady=(20, 0), padx=40, anchor="w")
        
        self.interval_entry = ctk.CTkEntry(self, width=370, height=40, corner_radius=10, border_width=2)
        self.interval_entry.insert(0, str(INTERVAL_MINUTES))
        self.interval_entry.pack(pady=(5, 15))

        # In here I have created input fields for the user to set the reminder interval and message.
        self.message_label = ctk.CTkLabel(self, text="Reminder Message", font=ctk.CTkFont(size=13, weight="bold"))
        self.message_label.pack(padx=40, anchor="w")
        
        self.message_entry = ctk.CTkEntry(self, width=370, height=40, corner_radius=10, border_width=2)
        self.message_entry.insert(0, MESSAGE)
        self.message_entry.pack(pady=(5, 20))

        # In here I have created a button frame to hold the Start and Stop buttons.
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10, padx=40, fill="x")

        # Green and Red buttons for Start and Stop
        self.start_btn = ctk.CTkButton(self.button_frame, text="START", command=self.start_reminder,
                                       fg_color=SUCCESS_GREEN, hover_color=SUCCESS_HOVER, 
                                       text_color="white", font=ctk.CTkFont(weight="bold"),
                                       height=45, corner_radius=10)
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.stop_btn = ctk.CTkButton(self.button_frame, text="STOP", command=self.stop_reminder,
                                      state="disabled", fg_color=DISABLED_GREY, 
                                      text_color="white", font=ctk.CTkFont(weight="bold"),
                                      height=45, corner_radius=10)
        self.stop_btn.pack(side="left", fill="x", expand=True)

        # Countdown - Set text color dynamically based on theme
        # Light mode = Dark text | Dark mode = Yellow text
        self.countdown_label = ctk.CTkLabel(self, text="Next reminder in: 00:00",
                                            font=ctk.CTkFont(size=18, weight="bold"),
                                            text_color=("#2B2B2B", GOLD)) 
        self.countdown_label.pack(pady=(25, 5))
        
        self.status_label = ctk.CTkLabel(self, text="Status: Stopped",
                                         font=ctk.CTkFont(size=12),
                                         text_color="grey")
        self.status_label.pack(pady=0)

        self.reminder = None
        self.running = False
        self.countdown_thread = None

#In here I have defined the function start_reminder that takes two optional parameters: interval_minutes and message. 
# The function will send notifications at regular intervals specified by interval_minutes, using the message provided. 
# If no parameters are given, it will use the default values from config.py.
    def start_reminder(self):
        try:
            interval = int(self.interval_entry.get())
            message = self.message_entry.get()
            if interval <= 0 or not message:
                raise ValueError
        except ValueError:
            return

        self.reminder = Reminder(interval, message)
        self.reminder.start()
        self.running = True
        
        self.start_btn.configure(state="disabled", fg_color=DISABLED_GREY)
        self.stop_btn.configure(state="normal", fg_color=DANGER_RED, hover_color=DANGER_HOVER)
        self.status_label.configure(text=f"Status: Running every {interval} min", text_color=SUCCESS_GREEN)

        self.countdown_thread = threading.Thread(target=self.update_countdown, args=(interval*60,), daemon=True)
        self.countdown_thread.start()

    def stop_reminder(self):
        if self.reminder: self.reminder.stop()
        self.running = False
        self.start_btn.configure(state="normal", fg_color=SUCCESS_GREEN)
        self.stop_btn.configure(state="disabled", fg_color=DISABLED_GREY)
        self.status_label.configure(text="Status: Stopped", text_color="grey")
        self.countdown_label.configure(text="Next reminder in: 00:00")

    def update_countdown(self, total_seconds):
        seconds_left = total_seconds
        while self.running and seconds_left > 0:
            mins, secs = divmod(seconds_left, 60)
            self.countdown_label.configure(text=f"Next reminder in: {mins:02d}:{secs:02d}")
            time.sleep(1)
            seconds_left -= 1
            if seconds_left <= 0: seconds_left = total_seconds

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")


#******* startup linux
#cd ~/.config/autostart
#nano script.desktop
##[Desktop Entry]
##Name=My Python Script
##Exec=python3 /path/to/your/script.py
##Type=Application
##X-GNOME-Autostart-enabled=true


#******* startup windows
#C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
## copy file here


#******* startup mcaOS
#/Users/YourUsername/Library/LaunchAgents
#create file com.example.script.plist
##<?xml version="1.0" encoding="UTF-8"?>
##<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
##<plist version="1.0">
##<dict>
##    <key>Label</key>
##    <string>com.example.script</string>
##    <key>ProgramArguments</key>
##    <array>
##        <string>python3</string>
##        <string>/path/to/your/script.py</string>
##    </array>
##    <key>RunAtLoad</key>
##    <true/>
##</dict>
##</plist>

import tkinter as tk
import time
from git import Repo
from datetime import datetime, timedelta
import os
last_check_time = datetime.now()
process_update = False
delay_duration = 24

class Update:
    def create_app(self):
        def update_message():
            global process_update
            label.config(text="Updating....")
            self.repo.git.pull()
            window.destroy()
            process_update = False
            os.system('reboot')

        def update_process():
            global process_update, last_check_time
            process_update = True
            last_check_time = datetime.now()
            window.destroy()

        window = tk.Tk()
        window.title("Update Alert")
        window.geometry("400x300")
        label = tk.Label(window, text="", font=("Arial", 14))
        label.pack(pady=20)
        var = tk.StringVar()
        label = tk.Message( window, textvariable=var, relief=tk.RAISED )
        var.set("Attention if you Update Now, It will restart the robot after finish update")
        label.pack()
        button_update = tk.Button(window, text="Update Now", command=update_message)
        button_update.pack(pady=10)
        button_stop = tk.Button(window, text="Update Later", command=update_process)
        button_stop.pack(pady=10)
        window.attributes('-topmost',True)
        window.mainloop()

    def check_for_update(self):
        global last_check_time, process_update
        current_time = datetime.now()
        time_difference = current_time - last_check_time
        if time_difference >= timedelta(hours=1):
            last_check_time = current_time
            self.repo = Repo()
            diff = self.repo.git.diff(self.repo.head)
            if diff:
                self.create_app()
            else:
                print('Up to date')

if __name__ == "__main__":
    update_instance = Update()
    while True:
        diftime = datetime.now() - last_check_time
        if (process_update == True) and (diftime >= timedelta(hours=delay_duration)):
            update_instance.create_app()

        elif (process_update == False):
            update_instance.check_for_update()
        time.sleep(5)

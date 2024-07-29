import tkinter as tk
from tkinter import simpledialog as sd
import webbrowser as wb
import subprocess as sp
import datetime as dt
import os

class ChatBot:
    def __init__(self, root):
        self.entry = None
        self.text = None
        self.root = root
        self.root.title("Chatbot")
        self.create_widgets()
        self.command_history = []

    def create_widgets(self):
        self.text = tk.Text(self.root, state='disabled', wrap='word')
        self.text.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.display_message(f'You: {user_input}')
        self.command_history.append(user_input)
        try:
            self.handle_input(user_input)
        except Exception as e:
            self.display_message(f"Error: {str(e)}")

    def display_message(self, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.config(state='disabled')
        self.text.yview(tk.END)

    def handle_input(self, user_input):
        user_input = user_input.lower()

        commands = {
            "show history": self.show_history,
            "show commands": self.show_commands,
            "open google": self.search_google,
            "search google": self.search_google,
            "open youtube": self.search_youtube,
            "search youtube": self.search_youtube,
            "open chrome": self.open_google_chrome,
            "open edge": self.open_microsoft_edge,
            "time": self.tell_time,
            "date": self.tell_date,
            "day": self.tell_day,
            "bye bye": self.exit_chatbot,
            "open file creator bot": self.open_file_creator_bot,
            "open website opener bot": self.open_website_opener_bot,
        }

        for command, action in commands.items():
            if command in user_input:
                action()
                return

        if "open" in user_input:
            self.open_application(user_input)
        elif "close" in user_input:
            self.close_application(user_input)
        else:
            try:
                result = self.safe_eval(user_input)
                self.display_message(f"The result is {result}")
            except Exception:
                self.display_message("Command not recognized or invalid math operation.")

    def safe_eval(self, expression):
        allowed_chars = "0123456789+-*/(). "
        if all(char in allowed_chars for char in expression):
            return eval(expression)
        else:
            raise ValueError("Invalid characters in math expression.")

    def show_history(self):
        self.display_message("Command history:")
        for i, command in enumerate(self.command_history, 1):
            self.display_message(f"{i}. {command}")

    def show_commands(self):
        commands = [
            "show history", "show commands", "open google",
            "search google", "open youtube", "search youtube", "open chrome",
            "open edge", "time", "date", "day", "bye bye",
            "open file creator bot", "open website opener bot"
        ]
        self.display_message("Available commands:")
        for command in commands:
            self.display_message(command)

    def search_google(self):
        query = sd.askstring("Input", "What do you want to search on Google?")
        if query and query.lower() != "nothing":
            wb.open(f"https://www.google.com/search?q={query}")
            self.display_message(f"Searching Google for: {query}")
        else:
            wb.open("https://www.google.com")
            self.display_message("Opening Google...")

    def search_youtube(self):
        query = sd.askstring("Input", "What do you want to search on YouTube?")
        if query and query.lower() != "nothing":
            wb.open(f"https://www.youtube.com/results?search_query={query}")
            self.display_message(f"Searching YouTube for: {query}")
        else:
            wb.open("https://www.youtube.com")
            self.display_message("Opening YouTube...")

    def open_google_chrome(self):
        sp.Popen(["start", "chrome"], shell=True)
        self.display_message("Opening Google Chrome...")

    def open_microsoft_edge(self):
        sp.Popen(["start", "msedge"], shell=True)
        self.display_message("Opening Microsoft Edge...")

    def open_application(self, user_input):
        applications = {
            "camera": "start microsoft.windows.camera:",
            "settings": "start ms-settings:",
            "file explorer": "explorer",
            "word": "start winword",
            "excel": "start excel",
            "powerpoint": "start powerpnt",
            "store": "start ms-windows-store:",
            "photos": "start ms-photos:",
            "xbox": "start xbox:",
            "clipchamp": "start ms-clipchamp:",
            "calculator": "calc",
            "clock": "start ms-clock:",
            "notepad": "notepad",
            "paint": "mspaint",
            "film & tv": "start mswindowsvideo:",
            "snipping tool": "snippingtool",
            "calendar": "start outlookcal:",
            "onenote": "start onenote:",
            "teams": "start teams",
            "vscode": "code",
            "autocad": "acad",
            "mcafee": "start mcafee",
            "glidex": "start glidex",
            "myasus": "start myasus",
            "screenxpert": "start screenxpert",
            "dev home": "start devhome",
            "amd software": "start amd-software",
            "alexa": "start alexa",
            "outlook": "start outlook",
            "zoom": "start zoom",
            "anaconda navigator": "anaconda-navigator",
            "powerbi": "start powerbi-desktop",
            "intellij": "idea",
            "pycharm": "pycharm",
            "cmd": "start cmd",
            "command prompt": "start cmd"
        }
        for key in applications:
            if key in user_input:
                sp.Popen(applications[key], shell=True)
                self.display_message(f"Opening {key}...")
                return
        self.display_message("The Application not recognized or not installed.")

    def close_application(self, user_input):
        applications = {
            "camera": "WindowsCamera.exe",
            "settings": "SystemSettings.exe",
            "file explorer": "explorer.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
            "store": "WinStore.App.exe",
            "photos": "Microsoft.Photos.exe",
            "xbox": "XboxApp.exe",
            "clipchamp": "Clipchamp.exe",
            "calculator": "Calculator.exe",
            "clock": "Time.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "film & tv": "Video.UI.exe",
            "snipping tool": "SnippingTool.exe",
            "calendar": "HxCalendarAppImm.exe",
            "onenote": "ONENOTE.EXE",
            "teams": "Teams.exe",
            "vscode": "Code.exe",
            "autocad": "acad.exe",
            "mcafee": "mcafee.exe",
            "glidex": "glidex.exe",
            "myasus": "myasus.exe",
            "screenxpert": "screenxpert.exe",
            "dev home": "devhome.exe",
            "amd software": "amd-software.exe",
            "alexa": "alexa.exe",
            "outlook": "OUTLOOK.EXE",
            "zoom": "zoom.exe",
            "anaconda navigator": "AnacondaNavigator.exe",
            "powerbi": "PBIDesktop.exe",
            "intellij": "idea64.exe",
            "pycharm": "pycharm64.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe"
        }
        for key in applications:
            if key in user_input:
                os.system(f"taskkill /f /im {applications[key]}")
                self.display_message(f"Closing {key}...")
                return
        self.display_message("The Application not recognized or not running.")

    def tell_time(self):
        now = dt.datetime.now().strftime("%I:%M:%S %p")
        self.display_message(f"The current time is {now}")

    def tell_date(self):
        today = dt.date.today().strftime("%B %d, %Y")
        self.display_message(f"Today's date is {today}")

    def tell_day(self):
        today = dt.datetime.today().strftime("%A")
        self.display_message(f"Today is {today}")

    def exit_chatbot(self):
        self.display_message("Goodbye!")
        self.root.quit()

    def open_file_creator_bot(self):
        sp.Popen(["python", "02_files.py"], shell=True)
        self.display_message("Opening File Creator Bot...")

    def open_website_opener_bot(self):
        sp.Popen(["python", "03_websites.py"], shell=True)
        self.display_message("Opening Website Opener Bot...")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = ChatBot(root)
    root.mainloop()

import tkinter as tk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
import os
import subprocess as sp
import re

class FileCreatorBot:
    def __init__(self, root):
        self.root = root
        self.root.title("File Creator Bot")
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
        self.display_message(f'You: {user_input}', sender='user')
        self.command_history.append(user_input)
        try:
            self.handle_input(user_input)
        except Exception as e:
            self.display_message(f"Error: {str(e)}", sender='bot')

    def display_message(self, message, sender='bot'):
        self.text.config(state='normal')
        if sender == 'bot':
            self.text.insert(tk.END, f'Bot: {message}\n')
        else:
            self.text.insert(tk.END, f'You: {message}\n')
        self.text.config(state='disabled')
        self.text.yview(tk.END)

    def handle_input(self, user_input):
        user_input = user_input.lower()
        command_map = {
            "create a folder": self.create_folder,
            "create a text file": lambda _: self.create_file(".txt"),
            "create an image file": lambda _: self.create_file(".bmp"),
            "create a zip file": lambda _: self.create_file(".zip"),
            "create a document file": lambda _: self.create_file(".docx"),
            "create an excel file": lambda _: self.create_file(".xlsx"),
            "create a presentation file": lambda _: self.create_file(".pptx"),
            "open folder": self.open_folder,
            "open file": self.open_file,
            "show history": self.show_history,
            "show commands": self.show_commands,
            "bye bye": self.exit_chatbot,
        }

        matched_command = None
        for command in command_map:
            if user_input.startswith(command):
                matched_command = command
                break

        if matched_command:
            try:
                arg = user_input.replace(matched_command, "").strip()
                command_map[matched_command](arg)
            except Exception as e:
                self.display_message(f"Error executing command '{matched_command}': {str(e)}")
        else:
            self.display_message("Command not recognized. Type 'show commands' to see available commands.")

    def is_valid_name(self, name):
        return re.match("^[A-Za-z0-9_-]*$", name) is not None

    def get_location(self, name):
        location = sd.askstring("Location", f"Where do you want to create/open the folder/file '{name}'?\nOptions: Desktop, Crazy Brain Cells, Stupid Codes, College, ChatGPT, Drone")
        if location:
            if not self.is_valid_name(location):
                self.display_message(f"Invalid location name: {location}")
                return None
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            if location.lower() == "desktop":
                return desktop_path
            else:
                folder_path = os.path.join(desktop_path, location)
                if os.path.exists(folder_path):
                    return folder_path
                else:
                    self.display_message(f"Folder '{location}' does not exist on the desktop.")
                    return None
        else:
            self.display_message("Location not specified.")
            return None

    def create_folder(self, arg=None):
        folder_name = sd.askstring("Folder Name", "Enter the name of the folder:")
        if folder_name:
            if mb.askokcancel("Confirmation", f"Do you really want to create the folder '{folder_name}'?"):
                location = self.get_location(folder_name)
                if location:
                    folder_path = os.path.join(location, folder_name)
                    try:
                        os.makedirs(folder_path, exist_ok=True)
                        self.display_message(f"Folder '{folder_name}' created at '{location}'.")
                    except Exception as e:
                        self.display_message(f"Error creating folder: {str(e)}")
            else:
                self.display_message("Folder creation canceled.")
        else:
            self.display_message("Folder name not specified.")

    def create_file(self, extension):
        file_name = sd.askstring("File Name", f"Enter the name of the {extension} file:")
        if file_name:
            if mb.askokcancel("Confirmation", f"Do you really want to create the file '{file_name}{extension}'?"):
                location = self.get_location(file_name)
                if location:
                    file_path = os.path.join(location, file_name + extension)
                    try:
                        with open(file_path, 'w') as f:
                            pass
                        self.display_message(f"File '{file_name}{extension}' created at '{location}'.")
                    except Exception as e:
                        self.display_message(f"Error creating file: {str(e)}")
            else:
                self.display_message("File creation canceled.")
        else:
            self.display_message("File name not specified.")

    def open_folder(self, folder_name):
        location = self.get_location(folder_name)
        if location:
            folder_path = os.path.join(location, folder_name)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                sp.Popen(f'explorer "{folder_path}"')
                self.display_message(f"Folder '{folder_name}' opened.")
            else:
                self.display_message(f"Folder '{folder_name}' does not exist at '{location}'.")

    def open_file(self, file_name):
        location = self.get_location(file_name)
        if location:
            matching_files = [f for f in os.listdir(location) if f.startswith(file_name)]
            if len(matching_files) == 0:
                self.display_message(f"No file named '{file_name}' found at '{location}'.")
            elif len(matching_files) == 1:
                file_path = os.path.join(location, matching_files[0])
                sp.Popen(f'start "" "{file_path}"', shell=True)
                self.display_message(f"File '{matching_files[0]}' opened.")
            else:
                self.display_message(f"Multiple files found with the name '{file_name}': {', '.join(matching_files)}")
                chosen_file = sd.askstring("Choose File", f"Multiple files found: {', '.join(matching_files)}\nWhich one do you want to open?")
                if chosen_file in matching_files:
                    file_path = os.path.join(location, chosen_file)
                    sp.Popen(f'start "" "{file_path}"', shell=True)
                    self.display_message(f"File '{chosen_file}' opened.")
                else:
                    self.display_message("File not recognized or not specified.")

    def show_history(self, arg=None):
        self.display_message("Command history:")
        for i, command in enumerate(self.command_history, 1):
            self.display_message(f"{i}. {command}")

    def show_commands(self, arg=None):
        commands_list = [
            "create a folder - Create a new folder",
            "create a text file - Create a new text file",
            "create an image file - Create a new image file",
            "create a zip file - Create a new zip file",
            "create a document file - Create a new document file",
            "create an excel file - Create a new Excel file",
            "create a presentation file - Create a new presentation file",
            "open folder {name_of_the_folder} - Open a folder",
            "open file {name_of_the_file} - Open a file",
            "show history - Show command history",
            "show commands - Show available commands",
            "bye bye - Terminate the bot"
        ]
        self.display_message("Available Commands:")
        for command in commands_list:
            self.display_message(command, sender='bot')

    def exit_chatbot(self, arg=None):
        self.display_message("Goodbye!")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    bot = FileCreatorBot(root)
    root.mainloop()

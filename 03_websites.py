import tkinter as tk
import webbrowser as wb

class ChatBot:
    def __init__(self, root):
        self.entry = None
        self.text = None
        self.root = root
        self.root.title("Website Opener Bot")
        self.create_widgets()

        self.website_urls = {
            "onlinegdb": "https://www.onlinegdb.com",
            "instagram": "https://www.instagram.com",
            "zotero": "https://zotero.org",
            "prezi": "https://prezi.com",
            "github copilot": "https://github.com/features/copilot",
            "tabnine": "https://tabnine.com",
            "kite": "https://open-vsx.org/",
            "canva": "https://canva.com",
            "gamma": "https://gamma.app",
            "zcode": "https://zzzcode.ai",
            "replit": "https://replit.com",
            "popai": "https://popai.pro",
            "blackboxai": "https://blackbox.ai",
            "github": "https://github.com",
            "leetcode": "https://leetcode.com",
            "codepen": "https://codepen.io",
            "amazon": "https://www.amazon.in",
            "zara": "https://www.zara.com",
            "ikea": "https://www.ikea.com",
            "hnm": "https://www2.hm.com",
            "copyai": "https://www.copy.ai",
            "quillbot": "https://quillbot.com",
        }

        self.command_map = {
            "open ": self.open_website,
            "bye bye": self.exit_chatbot,
            "help": self.show_help,
            "thank you": self.initiate_termination,
            "i am done": self.initiate_termination,
            "exit please": self.initiate_termination,
            "goodbye": self.initiate_termination,
            "end session": self.initiate_termination,
        }

        self.termination_state = None

    def create_widgets(self):
        self.text = tk.Text(self.root, state='disabled', wrap='word')
        self.text.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.process_input)

    def process_input(self, event):
        user_input = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        self.display_message(f'You: {user_input}')

        if self.termination_state:
            self.handle_termination_state(user_input)
            return

        for command, func in self.command_map.items():
            if user_input.startswith(command):
                func(user_input)
                break
        else:
            self.display_message("Command not recognized. Type 'help' to see available commands.")

    def display_message(self, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, message + "\n")
        self.text.config(state='disabled')
        self.text.yview(tk.END)

    def open_website(self, user_input):
        website_name = user_input.split("open ", 1)[1].strip()
        url = self.website_urls.get(website_name)
        if url:
            try:
                wb.open(url)
                self.display_message(f"Opening {website_name}...")
            except Exception as e:
                self.display_message(f"Failed to open {website_name}: {str(e)}")
        else:
            self.display_message(f"{website_name} not found in the list. Type 'help' to see available websites.")

    def exit_chatbot(self, user_input=None):
        self.display_message("Bot: Bye bye!")
        self.root.quit()

    def show_help(self, user_input=None):
        help_message = "Available commands:\n"
        for website in self.website_urls:
            help_message += f"open {website} - Open {website}\n"
        help_message += (
            "bye bye - Exit the bot\n"
            "thank you - Initiate termination process\n"
            "i am done - Initiate termination process\n"
            "exit please - Initiate termination process\n"
            "goodbye - Initiate termination process\n"
            "end session - Initiate termination process\n"
        )
        self.display_message(help_message)

    def initiate_termination(self, user_input):
        self.display_message("Bot: Are you sure you want to exit? (yes/no)")
        self.termination_state = 'confirm_exit'

    def handle_termination_state(self, user_input):
        if self.termination_state == 'confirm_exit':
            if user_input == "yes":
                self.exit_chatbot()
            else:
                self.display_message("Bot: Termination cancelled.")
            self.termination_state = None

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = ChatBot(root)
    root.mainloop()

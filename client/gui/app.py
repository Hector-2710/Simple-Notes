import tkinter as tk
from .components.auth import AuthFrame
from .components.notes import NotesFrame

class SimpleNotesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Notes")
        self.user_token = None
        self.geometry("600x700")
        self.container = tk.Frame(self)
        self.container.pack()
    
        self.show_auth()

    def show_auth(self):
        self._clear_screen()
        auth = AuthFrame(self.container, on_success=self.login_success)
        auth.pack(expand=True, fill="both")

    def login_success(self, data):
        self.user_token = data.get("access_token")
        self.show_notes() 

    def show_notes(self):
        self._clear_screen() 
        notes_frame = NotesFrame(self.container, self.user_token)
        notes_frame.pack(expand=True, fill="both")

    def _clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()
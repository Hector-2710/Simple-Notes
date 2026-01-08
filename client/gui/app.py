import tkinter as tk
from .components import AuthFrame

class SimpleNotesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user_token = None
        self.geometry("400x500")
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        
        self.show_auth()

    def show_auth(self):
        self._clear_screen()
        # 2. Le pasamos al hijo la función 'self.login_success' como un "callback"
        auth = AuthFrame(self.container, on_success=self.login_success)
        auth.pack()

    # 3. ESTA es la función que modifica el token
    def login_success(self, data):
        # 'data' es lo que devolvió la API (el JSON con el token e ID)
        self.user_token = data.get("access_token")
        self.user_id = data.get("id")
        
        print(f"Token guardado en App: {self.user_token}") # Debug
        self.show_notes() # Cambiamos de pantalla

    def show_notes(self):
        self._clear_screen()
        tk.Label(self.container, text="¡Estás dentro!").pack()
        # Aquí crearías el frame de notas pasándole el token si lo necesita

    def _clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()
import tkinter as tk
from tkinter import messagebox
import requests

class SimpleNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notes - Python Stack")
        self.root.geometry("400x500")
        self.current_user_id = None
        
        # URL de tu API de FastAPI
        self.base_url = "http://127.0.0.1:8000"
        
        # Variables de estado
        self.current_user_id = None
        
        # Widgets
        self.setup_ui()

    def setup_ui(self):
        # --- Sección de Usuario ---
        tk.Label(self.root, text="Username:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        tk.Label(self.root, text="Email:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        tk.Button(self.root, text="Register/Login", command=self.login_user, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- Sección de Notas ---
        tk.Label(self.root, text="Note Title:").pack()
        self.entry_title = tk.Entry(self.root)
        self.entry_title.pack()

        tk.Label(self.root, text="Content:").pack()
        self.text_content = tk.Text(self.root, height=5, width=30)
        self.text_content.pack(pady=5)

        tk.Button(self.root, text="Save Note", command=self.save_note, bg="#2196F3", fg="white").pack(pady=10)

    def login_user(self):
        payload = {
            "username": self.entry_username.get(),
            "email": self.entry_email.get()
        }
        try:
            # Llamada al endpoint de usuarios
            response = requests.post(f"{self.base_url}/users", json=payload)
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                print(data)
                # Aquí asumimos que tu API devuelve el ID. 
                # Si no lo devuelve, deberías ajustar el Schema de FastAPI.
                messagebox.showinfo("Success", "Logged in successfully!")
                print(data.get("id"))
                self.current_user_id = data.get("id")  # Ajusta según la respuesta real
            else:
                error = response.json().get("detail", "Unknown error")
                messagebox.showerror("Error", f"Failed: {error}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "API is not running!")

    def save_note(self):
        # Para este ejemplo, enviamos la nota al endpoint general
        payload = {
            "title": self.entry_title.get(),
            "content": self.text_content.get("1.0", tk.END).strip()
        }
        
        response = requests.post(f"{self.base_url}/notes/{self.current_user_id}", json=payload)
        print(self.current_user_id)
        
        if response.status_code == 200:
            messagebox.showinfo("Saved", "Note stored in PostgreSQL!")
            self.entry_title.delete(0, tk.END)
            self.text_content.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Could not save note")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotesApp(root)
    root.mainloop()
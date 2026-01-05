import tkinter as tk
from tkinter import messagebox
import requests

class SimpleNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notes")
        self.root.geometry("400x500")
        self.current_user_id = None
        self.base_url = "http://127.0.0.1:8000"
        self.current_mode = "login" 
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.setup_main_ui()

    def setup_main_ui(self):
        title_label = tk.Label(self.main_frame, text="Simple Notes", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        selection_frame = tk.Frame(self.main_frame)
        selection_frame.pack(pady=10)
        
        self.login_btn = tk.Button(selection_frame, text="Login", command=self.show_login_form, 
                                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'), width=10)
        self.login_btn.pack(side=tk.LEFT, padx=5)
        
        self.register_btn = tk.Button(selection_frame, text="Register", command=self.show_register_form,
                                     bg="#2196F3", fg="white", font=('Arial', 10, 'bold'), width=10)
        self.register_btn.pack(side=tk.LEFT, padx=5)
        
        separator = tk.Frame(self.main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, pady=15)
        
        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.pack(expand=True, fill='both')
        
        self.show_login_form()

    def clear_form_frame(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.clear_form_frame()
        
        self.login_btn.config(bg="#4CAF50", relief=tk.RAISED)
        self.register_btn.config(bg="#2196F3", relief=tk.FLAT)
        
        form_title = tk.Label(self.form_frame, text="Iniciar Sesión", font=('Arial', 14, 'bold'))
        form_title.pack(pady=10)
        
        tk.Label(self.form_frame, text="Email:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.entry_email = tk.Entry(self.form_frame, font=('Arial', 10), width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self.form_frame, text="Password:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.entry_password = tk.Entry(self.form_frame, font=('Arial', 10), width=30, show="*")
        self.entry_password.pack(pady=5)

        login_button = tk.Button(self.form_frame, text="Iniciar Sesión", command=self.login_user, 
                                bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'), width=15)
        login_button.pack(pady=20)

    def show_register_form(self):
        self.clear_form_frame()
        
        self.register_btn.config(bg="#2196F3", relief=tk.RAISED)
        self.login_btn.config(bg="#4CAF50", relief=tk.FLAT)
        
        form_title = tk.Label(self.form_frame, text="Registrarse", font=('Arial', 14, 'bold'))
        form_title.pack(pady=10)

        tk.Label(self.form_frame, text="Username:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.entry_username = tk.Entry(self.form_frame, font=('Arial', 10), width=30)
        self.entry_username.pack(pady=5)
        
        tk.Label(self.form_frame, text="Email:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.entry_email = tk.Entry(self.form_frame, font=('Arial', 10), width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self.form_frame, text="Password:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.entry_password = tk.Entry(self.form_frame, font=('Arial', 10), width=30, show="*")
        self.entry_password.pack(pady=5)

        register_button = tk.Button(self.form_frame, text="Registrarse", command=self.register_user,
                                   bg="#2196F3", fg="white", font=('Arial', 10, 'bold'), width=15)
        register_button.pack(pady=20)

    def login_user(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return
        
        payload = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(f"{self.base_url}/users/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.current_user_id = data.get("id") or data.get("user_id")
                messagebox.showinfo("Éxito", f"¡Bienvenido! ID de usuario: {self.current_user_id}")
                self.show_notes_interface()
            else:
                error = response.json().get("detail", "Credenciales incorrectas")
                messagebox.showerror("Error", f"Error de login: {error}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se puede conectar con la API. Asegúrate de que esté ejecutándose.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def register_user(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return
        
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(f"{self.base_url}/users", json=payload)
            
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                self.current_user_id = data.get("id") or data.get("user_id")
                messagebox.showinfo("Éxito", f"¡Usuario registrado exitosamente! ID: {self.current_user_id}")
                self.show_notes_interface()
            else:
                error = response.json().get("detail", "Error en el registro")
                messagebox.showerror("Error", f"Error de registro: {error}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se puede conectar con la API. Asegúrate de que esté ejecutándose.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def show_notes_interface(self):
        """Muestra la interfaz de notas después de login/registro exitoso"""
        self.clear_form_frame()
        
        # Información del usuario
        user_info = tk.Label(self.form_frame, text=f"Usuario ID: {self.current_user_id}", 
                            font=('Arial', 10, 'bold'), fg="#4CAF50")
        user_info.pack(pady=10)
        
        # Botón de logout
        logout_btn = tk.Button(self.form_frame, text="Cerrar Sesión", command=self.logout,
                              bg="#f44336", fg="white", font=('Arial', 9))
        logout_btn.pack(pady=5)
        
        # Aquí puedes agregar la interfaz de notas
        tk.Label(self.form_frame, text="Gestión de Notas", font=('Arial', 12, 'bold')).pack(pady=15)
        
        # Ejemplo de campo para notas
        tk.Label(self.form_frame, text="Título de la nota:", font=('Arial', 10)).pack()
        self.entry_title = tk.Entry(self.form_frame, font=('Arial', 10), width=30)
        self.entry_title.pack(pady=5)
        
        tk.Label(self.form_frame, text="Contenido:", font=('Arial', 10)).pack()
        self.text_content = tk.Text(self.form_frame, height=6, width=35)
        self.text_content.pack(pady=5)
        
        save_btn = tk.Button(self.form_frame, text="Guardar Nota", command=self.save_note,
                            bg="#4CAF50", fg="white", font=('Arial', 10))
        save_btn.pack(pady=10)

    def logout(self):
        self.current_user_id = None
        self.show_login_form()

    def save_note(self):
        """Guarda una nota usando el ID del usuario logueado"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Debes estar logueado para guardar notas")
            return
            
        title = self.entry_title.get().strip()
        content = self.text_content.get("1.0", tk.END).strip()
        
        if not title or not content:
            messagebox.showerror("Error", "Por favor, completa el título y contenido")
            return
        
        payload = {
            "title": title,
            "content": content
        }
        
        try:
            response = requests.post(f"{self.base_url}/notes/{self.current_user_id}", json=payload)
            
            if response.status_code == 200 or response.status_code == 201:
                messagebox.showinfo("Éxito", "¡Nota guardada correctamente!")
                self.entry_title.delete(0, tk.END)
                self.text_content.delete("1.0", tk.END)
            else:
                error = response.json().get("detail", "Error al guardar la nota")
                messagebox.showerror("Error", f"No se pudo guardar: {error}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No se puede conectar con la API")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotesApp(root)
    root.mainloop()
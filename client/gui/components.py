import tkinter as tk
from tkinter import messagebox
from api_client.services import login_user_api, register_user_api

class AuthFrame(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success
        self.setup_ui()


    def setup_ui(self):
        # Botones de selección superiores
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Login", command=self.show_login_form, bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.show_register_form, bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        
        self.form_container = tk.Frame(self)
        self.form_container.pack(fill="both", expand=True)
        self.show_login_form()

    def clear_form(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()

    def show_login_form(self):
        self.clear_form()
        tk.Label(self.form_container, text="Iniciar Sesión", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(self.form_container, text="Email:").pack()
        self.entry_email = tk.Entry(self.form_container, width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self.form_container, text="Password:").pack()
        self.entry_pass = tk.Entry(self.form_container, width=30, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(self.form_container, text="Entrar", bg="#4CAF50", fg="white", command=self._handle_login).pack(pady=20)

    def show_register_form(self):
        self.clear_form()
        tk.Label(self.form_container, text="Registrarse", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(self.form_container, text="Username:").pack()
        self.entry_user = tk.Entry(self.form_container, width=30)
        self.entry_user.pack(pady=5)

        tk.Label(self.form_container, text="Email:").pack()
        self.entry_email = tk.Entry(self.form_container, width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self.form_container, text="Password:").pack()
        self.entry_pass = tk.Entry(self.form_container, width=30, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(self.form_container, text="Crear Cuenta", bg="#2196F3", fg="white", command=self._handle_register).pack(pady=20)

    def _handle_login(self):
        res = login_user_api(self.entry_email.get(), self.entry_pass.get())
        if res.status_code == 200:
            self.on_success(res.json())

        else:
            messagebox.showerror("Error", "Login fallido")

    def _handle_register(self):
        res = register_user_api(self.entry_user.get(), self.entry_email.get(), self.entry_pass.get())
        if res.status_code in [200, 201]:
            messagebox.showinfo("Éxito", "Registrado. Ahora inicia sesión.")
            self.show_login_form()
            self.on_success(res.json())
        else:
            messagebox.showerror("Error", "Error al registrar")
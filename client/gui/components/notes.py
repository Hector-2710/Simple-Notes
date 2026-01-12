import tkinter as tk
from tkinter import messagebox, scrolledtext
from api_client.services import get_notes_api, save_note_api, delete_note_api

class NotesFrame(tk.Frame):
    def __init__(self, parent, token):
        super().__init__(parent)
        self.token = token
        self.notes = []
        self.setup_ui()
        self.refresh_notes()

    def setup_ui(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header, text="Mis Notas", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="Nueva Nota", bg="#4CAF50", fg="white", 
                 command=self.show_add_note_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar", bg="#2196F3", fg="white", 
                 command=self.refresh_notes).pack(side=tk.LEFT, padx=5)
        
        self.notes_container = tk.Frame(self)
        self.notes_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.canvas = tk.Canvas(self.notes_container)
        self.scrollbar = tk.Scrollbar(self.notes_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def refresh_notes(self):
        try:
            response = get_notes_api(self.token)
            if response.status_code == 200:
                self.notes = response.json()
                self.display_notes()
            else:
                messagebox.showerror("Error", "No se pudieron cargar las notas")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")
    
    def display_notes(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.notes:
            tk.Label(self.scrollable_frame, text="No tienes notas aún", 
                    font=('Arial', 12), fg="gray").pack(pady=20)
            return
        
        for note in self.notes:
            self.create_note_widget(note)
    
    def create_note_widget(self, note):
        note_frame = tk.Frame(self.scrollable_frame, relief="raised", bd=1, bg="white")
        note_frame.pack(fill="x", pady=5, padx=5)
        
        header = tk.Frame(note_frame, bg="white")
        header.pack(fill="x", padx=10, pady=5)
        
        title_label = tk.Label(header, text=note["title"], font=('Arial', 12, 'bold'), bg="white")
        title_label.pack(side=tk.LEFT)
        
        delete_btn = tk.Button(header, text="✗", fg="red", bg="white", 
                              command=lambda: self.delete_note(note["title"]),
                              font=('Arial', 10, 'bold'), bd=0)
        delete_btn.pack(side=tk.RIGHT)
        
        content = note["content"]
        if len(content) > 100:
            content = content[:100] + "..."
        
        content_label = tk.Label(note_frame, text=content, wraplength=350, 
                                justify=tk.LEFT, bg="white", fg="gray")
        content_label.pack(fill="x", padx=10, pady=(0, 10))
        
        note_frame.bind("<Button-1>", lambda e: self.view_note(note))
        title_label.bind("<Button-1>", lambda e: self.view_note(note))
        content_label.bind("<Button-1>", lambda e: self.view_note(note))

    def view_note(self, note):
        # Create a popup window to view the full note
        popup = tk.Toplevel(self)
        popup.title(f"Nota: {note['title']}")
        popup.geometry("500x400")
        
        # Title
        tk.Label(popup, text=note["title"], font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Content
        content_text = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=60, height=20)
        content_text.pack(fill="both", expand=True, padx=10, pady=10)
        content_text.insert(tk.END, note["content"])
        content_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(popup, text="Cerrar", command=popup.destroy).pack(pady=10)
    
    def show_add_note_dialog(self):
        # Clear the current content and show add note form
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Create form container (centrado con ancho limitado)
        container = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        container.pack(fill="x", pady=10)
        
        form_frame = tk.Frame(container, bg="white", relief="raised", bd=1)
        form_frame.pack(padx=50, pady=5)  # Margins para centrar y limitar ancho
        
        # Form header
        header_frame = tk.Frame(form_frame, bg="white")
        header_frame.pack(padx=20, pady=10)
        
        tk.Label(header_frame, text="Nueva Nota", font=('Arial', 12, 'bold'), bg="white").pack()
        
        # Title input
        title_frame = tk.Frame(form_frame, bg="white")
        title_frame.pack(padx=20, pady=5)
        
        tk.Label(title_frame, text="Título:", font=('Arial', 9), bg="white").pack(anchor="w")
        title_entry = tk.Entry(title_frame, font=('Arial', 9), width=35)
        title_entry.pack(pady=(2, 0))
        
        # Content input
        content_frame = tk.Frame(form_frame, bg="white")
        content_frame.pack(padx=20, pady=5)
        
        tk.Label(content_frame, text="Contenido:", font=('Arial', 9), bg="white").pack(anchor="w")
        content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=4, font=('Arial', 8), width=35)
        content_text.pack(pady=(2, 0))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(padx=20, pady=10)
        
        def save_note():
            title = title_entry.get().strip()
            content = content_text.get(1.0, tk.END).strip()
            
            if not title or not content:
                messagebox.showerror("Error", "Por favor completa todos los campos")
                return
            
            try:
                response = save_note_api(self.token, title, content)
                if response.status_code in [200, 201]:
                    messagebox.showinfo("Éxito", "Nota guardada exitosamente")
                    self.refresh_notes()  # Return to notes list
                else:
                    messagebox.showerror("Error", "No se pudo guardar la nota")
            except Exception as e:
                messagebox.showerror("Error", f"Error de conexión: {str(e)}")
        
        def cancel_add_note():
            self.display_notes()  # Return to notes list
        
        # Botones más pequeños y compactos
        tk.Button(btn_frame, text="Guardar", bg="#4CAF50", fg="white", 
                 command=save_note, font=('Arial', 8), width=10, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", bg="#f44336", fg="white", 
                 command=cancel_add_note, font=('Arial', 8), width=10, height=1).pack(side=tk.LEFT, padx=5)
        
        # Focus on title entry
        title_entry.focus_set()
    
    def delete_note(self, title):
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar la nota '{title}'?"):
            try:
                response = delete_note_api(self.token, title)
                if response.status_code == 200:
                    messagebox.showinfo("Éxito", "Nota eliminada exitosamente")
                    self.refresh_notes()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la nota")
            except Exception as e:
                messagebox.showerror("Error", f"Error de conexión: {str(e)}")
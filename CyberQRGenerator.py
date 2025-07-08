import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import os

class CyberQRGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔒 CyberQR Generator - Generador de Códigos QR Seguro")
        self.root.geometry("800x700")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        # Colores del tema ciberseguridad
        self.colors = {
            'bg_primary': '#0a0a0a',      # Negro profundo
            'bg_secondary': '#1a1a1a',    # Gris muy oscuro
            'bg_card': '#2a2a2a',         # Gris oscuro
            'accent_green': '#00ff41',    # Verde matrix
            'accent_blue': '#00d4ff',     # Azul cibernético
            'accent_red': '#ff3333',      # Rojo alerta
            'text_primary': '#ffffff',    # Blanco
            'text_secondary': '#b0b0b0',  # Gris claro
            'border': '#444444'           # Gris medio
        }
        
        self.qr_image = None
        self.setup_ui()
    
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=80)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔒 CYBERQR GENERATOR",
            font=('Consolas', 20, 'bold'),
            fg=self.colors['accent_green'],
            bg=self.colors['bg_primary']
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Generador de Códigos QR para Ciberseguridad",
            font=('Consolas', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        subtitle_label.pack()
        
        # Frame principal de contenido
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Configuración
        left_panel = tk.Frame(main_frame, bg=self.colors['bg_card'], width=350)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Panel derecho - Vista previa
        right_panel = tk.Frame(main_frame, bg=self.colors['bg_card'])
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=40)
        footer_frame.pack(fill='x', padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="⚡ Desarrollado para profesionales de ciberseguridad",
            font=('Consolas', 8),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        footer_label.pack(expand=True)
    
    def setup_left_panel(self, parent):
        # Título del panel
        panel_title = tk.Label(
            parent,
            text="⚙️ CONFIGURACIÓN",
            font=('Consolas', 12, 'bold'),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_card']
        )
        panel_title.pack(pady=(20, 15))
        
        # URL Input
        url_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        url_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        url_label = tk.Label(
            url_frame,
            text="🌐 URL o Texto:",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        url_label.pack(anchor='w')
        
        self.url_entry = tk.Text(
            url_frame,
            height=4,
            font=('Consolas', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_green'],
            relief='flat',
            bd=2,
            highlightthickness=1,
            highlightcolor=self.colors['accent_green']
        )
        self.url_entry.pack(fill='x', pady=(5, 0))
        
        # Tamaño del QR
        size_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        size_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        size_label = tk.Label(
            size_frame,
            text="📏 Tamaño del QR:",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        size_label.pack(anchor='w')
        
        self.size_var = tk.StringVar(value="10")
        size_scale = tk.Scale(
            size_frame,
            from_=5,
            to=20,
            orient='horizontal',
            variable=self.size_var,
            font=('Consolas', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_green'],
            highlightthickness=0,
            troughcolor=self.colors['bg_primary']
        )
        size_scale.pack(fill='x', pady=(5, 0))
        
        # Nivel de corrección de errores
        error_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        error_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        error_label = tk.Label(
            error_frame,
            text="🛡️ Corrección de Errores:",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        error_label.pack(anchor='w')
        
        self.error_var = tk.StringVar(value="M")
        error_options = ["L (Baja)", "M (Media)", "Q (Alta)", "H (Máxima)"]
        error_combo = ttk.Combobox(
            error_frame,
            textvariable=self.error_var,
            values=error_options,
            state='readonly',
            font=('Consolas', 9)
        )
        error_combo.pack(fill='x', pady=(5, 0))
        
        # Colores del QR
        color_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        color_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        color_label = tk.Label(
            color_frame,
            text="🎨 Tema de Color:",
            font=('Consolas', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        color_label.pack(anchor='w')
        
        self.color_var = tk.StringVar(value="Matrix Verde")
        color_options = ["Matrix Verde", "Cyber Azul", "Hacker Rojo", "Clásico B/N"]
        color_combo = ttk.Combobox(
            color_frame,
            textvariable=self.color_var,
            values=color_options,
            state='readonly',
            font=('Consolas', 9)
        )
        color_combo.pack(fill='x', pady=(5, 0))
        
        # Botones de acción
        button_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        button_frame.pack(fill='x', padx=20, pady=(20, 0))
        
        generate_btn = tk.Button(
            button_frame,
            text="🔄 GENERAR QR",
            command=self.generate_qr,
            font=('Consolas', 11, 'bold'),
            bg=self.colors['accent_green'],
            fg=self.colors['bg_primary'],
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        generate_btn.pack(fill='x', pady=(0, 10))
        
        save_btn = tk.Button(
            button_frame,
            text="💾 GUARDAR QR",
            command=self.save_qr,
            font=('Consolas', 11, 'bold'),
            bg=self.colors['accent_blue'],
            fg=self.colors['bg_primary'],
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        save_btn.pack(fill='x')
    
    def setup_right_panel(self, parent):
        # Título del panel
        panel_title = tk.Label(
            parent,
            text="👁️ VISTA PREVIA",
            font=('Consolas', 12, 'bold'),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_card']
        )
        panel_title.pack(pady=(20, 15))
        
        # Frame para el QR
        self.qr_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        self.qr_frame.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        # Etiqueta para mostrar el QR
        self.qr_label = tk.Label(
            self.qr_frame,
            text="🔍\n\nGenera un código QR\npara ver la vista previa",
            font=('Consolas', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            justify='center'
        )
        self.qr_label.pack(expand=True)
        
        # Info del QR
        self.info_label = tk.Label(
            parent,
            text="",
            font=('Consolas', 8),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_card'],
            justify='center'
        )
        self.info_label.pack(pady=(0, 20))
    
    def get_qr_colors(self, theme):
        """Obtiene los colores según el tema seleccionado"""
        color_schemes = {
            "Matrix Verde": ('#00ff41', '#000000'),
            "Cyber Azul": ('#00d4ff', '#001122'),
            "Hacker Rojo": ('#ff3333', '#220000'),
            "Clásico B/N": ('#000000', '#ffffff')
        }
        return color_schemes.get(theme, ('#000000', '#ffffff'))
    
    def get_error_correction(self, level):
        """Obtiene el nivel de corrección de errores"""
        levels = {
            "L (Baja)": qrcode.constants.ERROR_CORRECT_L,
            "M (Media)": qrcode.constants.ERROR_CORRECT_M,
            "Q (Alta)": qrcode.constants.ERROR_CORRECT_Q,
            "H (Máxima)": qrcode.constants.ERROR_CORRECT_H
        }
        return levels.get(level, qrcode.constants.ERROR_CORRECT_M)
    
    def generate_qr(self):
        try:
            # Obtener datos del formulario
            url_text = self.url_entry.get(1.0, tk.END).strip()
            
            if not url_text:
                messagebox.showwarning("⚠️ Advertencia", "Por favor ingresa una URL o texto")
                return
            
            # Configurar QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=self.get_error_correction(self.error_var.get()),
                box_size=int(self.size_var.get()),
                border=4
            )
            
            qr.add_data(url_text)
            qr.make(fit=True)
            
            # Obtener colores
            fg_color, bg_color = self.get_qr_colors(self.color_var.get())
            
            # Crear imagen
            self.qr_image = qr.make_image(fill_color=fg_color, back_color=bg_color)
            
            # Redimensionar para mostrar
            display_size = (300, 300)
            display_image = self.qr_image.resize(display_size, Image.Resampling.NEAREST)
            
            # Convertir para tkinter
            photo = ImageTk.PhotoImage(display_image)
            
            # Actualizar la vista previa
            self.qr_label.configure(image=photo, text="")
            self.qr_label.image = photo  # Mantener referencia
            
            # Actualizar información
            info_text = f"✅ QR generado exitosamente\n"
            info_text += f"📊 Tamaño: {self.qr_image.size[0]}x{self.qr_image.size[1]} px\n"
            info_text += f"🎨 Tema: {self.color_var.get()}\n"
            info_text += f"🛡️ Corrección: {self.error_var.get()}"
            
            self.info_label.configure(text=info_text)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al generar QR: {str(e)}")
    
    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("⚠️ Advertencia", "Primero genera un código QR")
            return
        
        try:
            # Diálogo para guardar archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ],
                title="Guardar Código QR"
            )
            
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("✅ Éxito", f"QR guardado en:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar: {str(e)}")
    
    def run(self):
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import qrcode
        from PIL import Image, ImageTk
    except ImportError as e:
        print("❌ Error: Dependencias faltantes")
        print("Instala las dependencias con:")
        print("pip install qrcode[pil] pillow")
        exit(1)
    
    # Crear y ejecutar la aplicación
    app = CyberQRGenerator()
    app.run()
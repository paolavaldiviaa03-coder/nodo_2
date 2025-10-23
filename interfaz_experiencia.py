#!/usr/bin/env python3
# =====================================================
# INTERFAZ GRÁFICA FULLSCREEN - EXPERIENCIA DE CLONACIÓN DE VOZ
# =====================================================
# Interfaz fullscreen con área para video externo

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import os
from pathlib import Path
import subprocess

# Importar el módulo de clonación de voz
try:
    # Agregar el directorio actual al path para importar
    sys.path.insert(0, str(Path(__file__).parent))
    from voice_cloner import VoiceCloner
except ImportError as e:
    print(f"Error al importar voice_cloner: {e}")
    print("Asegúrate de que voice_cloner.py existe en el mismo directorio")
    sys.exit(1)

class ExperienciaVozApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.voice_cloner = None
        self.proceso_activo = False
        self.video_process = None
        
    def setup_window(self):
        """Configurar la ventana principal en fullscreen"""
        self.root.title("🎤 Experiencia de Clonación de Voz - Nodo 2")
        
        # Configurar fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000')  # Fondo negro completo
        
        # Obtener dimensiones de pantalla
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Escape para salir de fullscreen (para desarrollo)
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
    def toggle_fullscreen(self):
        """Alternar modo fullscreen (solo para desarrollo)"""
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)
        
    def setup_styles(self):
        """Configurar estilos para fullscreen"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores para pantalla completa
        self.style.configure('FullTitle.TLabel', 
                           background='#000000', 
                           foreground='#ffffff',
                           font=('Arial', 48, 'bold'))
        
        self.style.configure('FullSubtitle.TLabel', 
                           background='#000000', 
                           foreground='#cccccc',
                           font=('Arial', 24))
        
        self.style.configure('FullStatus.TLabel', 
                           background='#000000', 
                           foreground='#00ff88',
                           font=('Arial', 20, 'bold'))
        
        self.style.configure('FullButton.TButton',
                           font=('Arial', 28, 'bold'),
                           padding=(40, 20))
        
    def create_widgets(self):
        """Crear interfaz fullscreen con área de video central"""
        # Frame principal que ocupa toda la pantalla
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True)
        
        # Título en la parte superior
        title_frame = tk.Frame(main_frame, bg='#000000', height=120)
        title_frame.pack(fill='x', side='top')
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, 
                               text="EXPERIENCIA DE CLONACIÓN DE VOZ", 
                               style='FullTitle.TLabel')
        title_label.pack(pady=(30, 10))
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="NODO 2 - LABORATORIO DE INTELIGENCIA ARTIFICIAL", 
                                  style='FullSubtitle.TLabel')
        subtitle_label.pack()
        
        # Área central para video
        video_frame = tk.Frame(main_frame, bg='#111111', relief='solid', bd=2)
        video_frame.pack(fill='both', expand=True, padx=100, pady=(50, 30))
        
        # Label para el área de video
        self.video_label = tk.Label(video_frame, 
                                   text="📹\n\nÁREA DE VIDEO\n\nAquí se reproducirá el video de instrucciones\ncuando inicies la experiencia",
                                   bg='#111111', 
                                   fg='#666666',
                                   font=('Arial', 24),
                                   justify='center')
        self.video_label.pack(fill='both', expand=True)
        
        # Frame inferior para botón y status
        bottom_frame = tk.Frame(main_frame, bg='#000000', height=180)
        bottom_frame.pack(fill='x', side='bottom')
        bottom_frame.pack_propagate(False)
        
        # Estado actual
        self.status_label = ttk.Label(bottom_frame, 
                                     text="✨ Presiona el botón para comenzar la experiencia", 
                                     style='FullStatus.TLabel')
        self.status_label.pack(pady=(20, 15))
        
        # Botón principal centrado
        self.start_button = ttk.Button(bottom_frame, 
                                      text="🚀 INICIAR EXPERIENCIA", 
                                      style='FullButton.TButton',
                                      command=self.iniciar_experiencia)
        self.start_button.pack(pady=10)
        
        # Barra de progreso (oculta inicialmente)
        self.progress_frame = tk.Frame(bottom_frame, bg='#000000')
        self.progress_frame.pack(fill='x', pady=10)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                           mode='indeterminate', 
                                           length=600)
        self.progress_bar.pack()
        self.progress_frame.pack_forget()  # Ocultar inicialmente
        
        # Instrucciones de salida (pequeñas en la esquina)
        exit_label = tk.Label(main_frame, 
                             text="Presiona ESC para salir", 
                             bg='#000000', fg='#444444', 
                             font=('Arial', 10))
        exit_label.place(relx=0.02, rely=0.02)
        
        # Bind para cerrar con ESC
        self.root.bind('<Escape>', lambda e: self.salir_aplicacion())
        
    def mostrar_video_en_area(self, mostrar=True, mensaje=""):
        """Mostrar/ocultar video en el área central"""
        if mostrar:
            if mensaje:
                self.video_label.config(text=mensaje, fg='#ffffff')
            else:
                self.video_label.config(text="🎬\n\nREPRODUCIENDO VIDEO\n\nMira las instrucciones atentamente", 
                                       fg='#00ff88')
        else:
            self.video_label.config(text="📹\n\nÁREA DE VIDEO\n\nAquí se reproducirá el video de instrucciones\ncuando inicies la experiencia",
                                   fg='#666666')
        
    def actualizar_status(self, mensaje):
        """Actualizar el mensaje de estado"""
        self.status_label.config(text=mensaje)
        self.root.update()
        
    def mostrar_progreso(self, mostrar=True):
        """Mostrar u ocultar la barra de progreso"""
        if mostrar:
            self.progress_frame.pack(fill='x', pady=10)
            self.progress_bar.start(10)
        else:
            self.progress_bar.stop()
            self.progress_frame.pack_forget()
            
    def iniciar_experiencia(self):
        """Iniciar la experiencia de clonación de voz en un hilo separado"""
        if self.proceso_activo:
            messagebox.showwarning("Advertencia", "Ya hay una experiencia en progreso")
            return
            
        # En modo fullscreen, confirmar de manera más sutil
        resultado = messagebox.askyesno(
            "Iniciar Experiencia", 
            "¿Estás listo para comenzar?\n\n" +
            "Necesitarás un micrófono y estar en silencio.\n" +
            "La experiencia durará aproximadamente 3 minutos."
        )
        
        if not resultado:
            return
            
        # Deshabilitar botón y mostrar progreso
        self.start_button.config(state='disabled')
        self.mostrar_progreso(True)
        self.proceso_activo = True
        
        # Ejecutar en hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.ejecutar_experiencia)
        thread.daemon = True
        thread.start()
            
    def salir_aplicacion(self):
        """Cerrar la aplicación con confirmación"""
        if self.proceso_activo:
            messagebox.showwarning(
                "Proceso Activo", 
                "Hay una experiencia en progreso. Espera a que termine antes de salir."
            )
            return
            
        # En fullscreen, salir directamente sin confirmación
        self.root.quit()
            
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🎤 Iniciando Experiencia de Clonación de Voz...")
    
    # Verificar dependencias básicas
    try:
        import pyaudio
        import requests
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias: {e}")
        print("Ejecuta: pip install -r requirements.txt")
        return
        
    # Iniciar aplicación
    app = ExperienciaVozApp()
    app.run()

if __name__ == "__main__":
    main()
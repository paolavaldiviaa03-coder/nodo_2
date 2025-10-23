#!/usr/bin/env python3
# =====================================================
# INTERFAZ GRÁFICA - EXPERIENCIA DE CLONACIÓN DE VOZ
# =====================================================
# Interfaz simple para la experiencia interactiva
# de clonación de voz usando ElevenLabs

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
        
    def setup_window(self):
        """Configurar la ventana principal"""
        self.root.title("🎤 Experiencia de Clonación de Voz - Nodo 2")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Hacer que no se pueda redimensionar
        self.root.resizable(False, False)
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores personalizados
        self.style.configure('Title.TLabel', 
                           background='#1a1a1a', 
                           foreground='#ffffff',
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel', 
                           background='#1a1a1a', 
                           foreground='#cccccc',
                           font=('Arial', 12))
        
        self.style.configure('Status.TLabel', 
                           background='#1a1a1a', 
                           foreground='#00ff88',
                           font=('Arial', 10, 'bold'))
        
        self.style.configure('Custom.TButton',
                           font=('Arial', 16, 'bold'),
                           padding=(20, 15))
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Logo/Título
        title_label = ttk.Label(main_frame, 
                               text="🎤 EXPERIENCIA DE CLONACIÓN DE VOZ", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = ttk.Label(main_frame, 
                                  text="Nodo 2 - Laboratorio de Inteligencia Artificial", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 40))
        
        # Descripción de la experiencia
        description_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='raised', bd=2)
        description_frame.pack(fill='x', pady=(0, 30), padx=20)
        
        desc_title = tk.Label(description_frame, 
                             text="¿Qué sucederá?", 
                             bg='#2a2a2a', fg='#ffffff', 
                             font=('Arial', 14, 'bold'))
        desc_title.pack(pady=(15, 10))
        
        steps_text = """
1. 📹 Se reproducirá un video con instrucciones
2. 🎙️ Grabaremos tu voz durante 13 segundos
3. 🤖 Tu voz será clonada usando Inteligencia Artificial
4. 🔊 Escucharás el resultado final
5. 🗑️ Tu voz será eliminada de nuestros servidores
        """
        
        steps_label = tk.Label(description_frame, 
                              text=steps_text, 
                              bg='#2a2a2a', fg='#cccccc', 
                              font=('Arial', 11),
                              justify='left')
        steps_label.pack(pady=(0, 15), padx=20)
        
        # Botón principal
        self.start_button = ttk.Button(main_frame, 
                                      text="🚀 INICIAR EXPERIENCIA", 
                                      style='Custom.TButton',
                                      command=self.iniciar_experiencia)
        self.start_button.pack(pady=30)
        
        # Barra de progreso
        self.progress_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.progress_frame.pack(fill='x', pady=(20, 0))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                           mode='indeterminate', 
                                           length=400)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()  # Ocultar inicialmente
        
        # Estado actual
        self.status_label = ttk.Label(main_frame, 
                                     text="✨ Listo para comenzar", 
                                     style='Status.TLabel')
        self.status_label.pack(pady=10)
        
        # Botón de salir
        exit_button = ttk.Button(main_frame, 
                                text="❌ Salir", 
                                command=self.salir_aplicacion)
        exit_button.pack(side='bottom', pady=(40, 0))
        
        # Log de actividad (oculto inicialmente)
        self.log_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.log_text = tk.Text(self.log_frame, 
                               height=8, 
                               bg='#000000', 
                               fg='#00ff88',
                               font=('Courier', 9),
                               wrap='word')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def actualizar_status(self, mensaje):
        """Actualizar el mensaje de estado"""
        self.status_label.config(text=mensaje)
        self.root.update()
        
    def mostrar_progreso(self, mostrar=True):
        """Mostrar u ocultar la barra de progreso"""
        if mostrar:
            self.progress_bar.pack(pady=10)
            self.progress_bar.start(10)
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            
    def log_mensaje(self, mensaje):
        """Agregar mensaje al log de actividad"""
        self.log_text.insert('end', f"{mensaje}\n")
        self.log_text.see('end')
        self.root.update()
        
    def mostrar_log(self, mostrar=True):
        """Mostrar u ocultar el log de actividad"""
        if mostrar:
            self.log_frame.pack(fill='both', expand=True, pady=(20, 0))
        else:
            self.log_frame.pack_forget()
            
    def iniciar_experiencia(self):
        """Iniciar la experiencia de clonación de voz en un hilo separado"""
        if self.proceso_activo:
            messagebox.showwarning("Advertencia", "Ya hay una experiencia en progreso")
            return
            
        # Confirmar inicio
        resultado = messagebox.askyesno(
            "Iniciar Experiencia", 
            "¿Estás listo para comenzar la experiencia de clonación de voz?\n\n" +
            "Necesitarás:\n" +
            "• Un micrófono funcionando\n" +
            "• Estar en un lugar tranquilo\n" +
            "• Conexión a internet\n\n" +
            "La experiencia durará aproximadamente 2-3 minutos."
        )
        
        if not resultado:
            return
            
        # Deshabilitar botón y mostrar progreso
        self.start_button.config(state='disabled')
        self.mostrar_progreso(True)
        self.mostrar_log(True)
        self.proceso_activo = True
        
        # Ejecutar en hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.ejecutar_experiencia)
        thread.daemon = True
        thread.start()
        
    def ejecutar_experiencia(self):
        """Ejecutar la experiencia completa de clonación de voz"""
        try:
            self.actualizar_status("🎬 Iniciando experiencia...")
            self.log_mensaje("=== EXPERIENCIA DE CLONACIÓN DE VOZ ===")
            
            # Crear instancia del clonador
            self.voice_cloner = VoiceCloner()
            
            # Ejecutar cada paso con actualizaciones de estado
            self.actualizar_status("📹 Reproduciendo video de instrucciones...")
            self.log_mensaje("PASO 1: Reproduciendo video de instrucciones")
            self.voice_cloner.reproducir_instrucciones()
            
            self.actualizar_status("🎙️ Preparando grabación de voz...")
            self.log_mensaje("PASO 2: Preparando grabación de voz")
            time.sleep(2)
            
            self.actualizar_status("🔴 GRABANDO VOZ - Habla ahora...")
            self.log_mensaje("PASO 3: GRABANDO VOZ (13 segundos)")
            archivo_voz = self.voice_cloner.grabar_voz()
            
            if not archivo_voz:
                raise Exception("Error en la grabación de voz")
                
            self.actualizar_status("☁️ Subiendo voz a la nube...")
            self.log_mensaje("PASO 4: Subiendo voz para clonación")
            voice_id = self.voice_cloner.clonar_voz(archivo_voz)
            
            if not voice_id:
                raise Exception("Error al clonar la voz")
                
            self.actualizar_status("🤖 Generando voz clonada...")
            self.log_mensaje("PASO 5: Generando audio con voz clonada")
            archivo_final = self.voice_cloner.sintetizar_voz(voice_id)
            
            if not archivo_final:
                raise Exception("Error al sintetizar la voz")
                
            self.actualizar_status("🔊 Reproduciendo resultado...")
            self.log_mensaje("PASO 6: Reproduciendo resultado final")
            self.voice_cloner.reproducir_resultado(archivo_final)
            
            self.actualizar_status("🗑️ Limpiando datos temporales...")
            self.log_mensaje("PASO 7: Eliminando voz de servidores")
            self.voice_cloner.limpiar_voz(voice_id)
            
            # Experiencia completada
            self.actualizar_status("✅ ¡Experiencia completada con éxito!")
            self.log_mensaje("=== EXPERIENCIA COMPLETADA ===")
            
            messagebox.showinfo(
                "¡Experiencia Completada!", 
                "Tu voz ha sido clonada exitosamente.\n\n" +
                "Recuerda que tu voz original ha sido eliminada\n" +
                "de nuestros servidores por privacidad.\n\n" +
                "¡Gracias por participar en nuestro experimento!"
            )
            
        except Exception as e:
            self.actualizar_status(f"❌ Error: {str(e)}")
            self.log_mensaje(f"ERROR: {str(e)}")
            messagebox.showerror(
                "Error en la Experiencia", 
                f"Ocurrió un error durante la experiencia:\n\n{str(e)}\n\n" +
                "Por favor, inténtalo de nuevo o contacta al administrador."
            )
            
        finally:
            # Restaurar interfaz
            self.mostrar_progreso(False)
            self.start_button.config(state='normal')
            self.proceso_activo = False
            
    def salir_aplicacion(self):
        """Cerrar la aplicación con confirmación"""
        if self.proceso_activo:
            messagebox.showwarning(
                "Proceso Activo", 
                "Hay una experiencia en progreso. Espera a que termine antes de salir."
            )
            return
            
        resultado = messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?")
        if resultado:
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
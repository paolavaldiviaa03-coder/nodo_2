import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import os
from pathlib import Path
import subprocess

# Importar la lógica de clonación de voz
try:
    # Agregar el directorio actual al path para importar
    sys.path.insert(0, str(Path(__file__).parent))
    from logica_clonacion import LogicaClonacion
except ImportError as e:
    print(f"Error al importar logica_clonacion: {e}")
    print("Asegúrate de que logica_clonacion.py existe en el mismo directorio")
    sys.exit(1)

class ExperienciaVozApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.logica_clonacion = None
        self.proceso_activo = False
        self.video_process = None
        
    def setup_window(self):
        """Configurar la ventana principal en fullscreen"""        
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
                           foreground="#2d3431",
                           font=('Arial', 20, 'bold'))
        
        self.style.configure('FullButton.TButton',
                           font=('Arial', 28, 'bold'),
                           padding=(40, 20))
        
    def create_widgets(self):
        # Frame principal que ocupa toda la pantalla
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True)
        
        # Título en la parte superior
        title_frame = tk.Frame(main_frame, bg='#000000', height=120)
        title_frame.pack(fill='x', side='top')
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, 
                               text="EXPERIENCIA NODO 2", 
                               style='FullTitle.TLabel')
        title_label.pack(pady=(30, 10))
        
        # Área central para video
        self.video_frame = tk.Frame(main_frame, bg='#111111', relief='solid', bd=2)
        self.video_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        # Label para el área de video (sin texto inicial para pantalla limpia)
        self.video_label = tk.Label(self.video_frame, 
                                   text="",
                                   bg='#111111', 
                                   fg='#666666',
                                   font=('Arial', 24),
                                   justify='center')
        self.video_label.pack(fill='both', expand=True)
        
        # Frame inferior para botón y status
        bottom_frame = tk.Frame(main_frame, bg='#000000', height=180)
        bottom_frame.pack(fill='x', side='bottom')
        bottom_frame.pack_propagate(False)
        
        # Botón principal centrado
        self.start_button = ttk.Button(bottom_frame, 
                                      text=" INICIAR EXPERIENCIA", 
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
        
        # Bind para cerrar con ESC
        self.root.bind('<Escape>', lambda e: self.salir_aplicacion())
        
    def mostrar_video_en_area(self, mostrar=True, mensaje=""):
        """Mostrar/ocultar contenido en el área central (sin texto adicional)"""
        if mostrar and mensaje:
            self.video_label.config(text=mensaje, fg='#ffffff', image="")
        elif not mostrar:
            self.video_label.config(text="", image="")
        
    def actualizar_status(self, mensaje):
        """Función placeholder para status (sin mostrar nada adicional)"""
        pass  # No mostrar status adicional como solicitado
        
        
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
            
        # Deshabilitar botón y mostrar progreso
        self.start_button.config(state='disabled')
        self.mostrar_progreso(True)
        self.proceso_activo = True
        
        # Ejecutar en hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self.ejecutar_experiencia)
        thread.daemon = True
        thread.start()
        
    def ejecutar_experiencia(self):
        """Ejecutar la experiencia completa de clonación de voz"""
        try:
            # Crear instancia del clonador
            self.logica_clonacion = LogicaClonacion()
            
            # PASO 1: Reproducir video en área central
            # Dar tiempo para que el frame se renderice completamente
            self.root.update()
            time.sleep(0.5)
            
            self.reproducir_video_integrado()
            
            # PASO 2: Video ya terminó (las funciones de reproducción esperan)
            # No necesitamos countdown adicional
            
            # PASO 3: Grabación
            archivo_voz = self.grabar_voz_con_visual()
            
            if not archivo_voz:
                raise Exception("Error en la grabación de voz")
                
            # PASO 4: Clonación
            voice_id = self.logica_clonacion.clonar_voz(archivo_voz)
            
            if not voice_id:
                raise Exception("Error al clonar la voz")
                
            # PASO 5: Síntesis
            archivo_final = self.logica_clonacion.sintetizar_voz(voice_id)
            
            if not archivo_final:
                raise Exception("Error al sintetizar la voz")
                
            # PASO 6: Reproducción
            self.logica_clonacion.reproducir_resultado(archivo_final)
            
            # PASO 7: Limpieza
            self.logica_clonacion.limpiar_voz(voice_id)
            
        except Exception as e:
            pass  # Manejo silencioso de errores
            
        finally:
            # Restaurar interfaz y limpiar procesos
            self.limpiar_procesos_multimedia()
            self.mostrar_progreso(False)
            self.start_button.config(state='normal')
            self.proceso_activo = False
            
    def reproducir_video_integrado(self):
        """Reproducir video integrado en el área de video"""
        video_file = 'instrucciones.mp4'
        
        if not os.path.exists(video_file):
            time.sleep(3)
            return
        
        # Para Raspberry Pi OS y sistemas Linux, usar reproductor externo para audio+video
        if sys.platform.startswith('linux'):
            self.reproducir_video_con_audio_linux(video_file)
        else:
            # Para otros sistemas, intentar OpenCV pero con audio externo
            try:
                import cv2
                from PIL import Image, ImageTk
                self.reproducir_video_con_opencv_y_audio(video_file)
            except ImportError:
                self.reproducir_video_placeholder(video_file)
            except Exception as e:
                self.reproducir_video_placeholder(video_file)
    
    def reproducir_video_con_audio_linux(self, video_file):
        """Reproducir video con audio completo en sistemas Linux/Raspberry Pi"""
        try:
            # Lista de reproductores de video disponibles en orden de preferencia
            reproductores = [
                ['omxplayer', '--no-osd', '--aspect-mode', 'letterbox'],  # Raspberry Pi específico
                ['vlc', '--play-and-exit', '--fullscreen', '--no-video-title'],  # VLC
                ['mpv', '--really-quiet', '--no-terminal'],  # MPV
                ['mplayer', '-quiet', '-really-quiet'],  # MPlayer
                ['ffplay', '-nodisp', '-autoexit']  # FFmpeg player (solo audio si no hay display)
            ]
            
            # Mostrar indicador visual mientras reproduce
            self.video_label.configure(
                text="ESCUCHA CON ATENCION", 
                fg="#da0d0d", 
                image=""
            )
            
            # Intentar cada reproductor hasta encontrar uno que funcione
            for cmd_base in reproductores:
                try:
                    cmd = cmd_base + [video_file]
                    
                    # Verificar si el comando existe
                    result = subprocess.run(['which', cmd_base[0]], 
                                          capture_output=True, 
                                          timeout=2)
                    
                    if result.returncode == 0:
                        print(f"Usando reproductor: {cmd_base[0]}")
                        
                        # Ejecutar el reproductor
                        self.video_process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                        )
                        
                        # Esperar a que termine (máximo 30 segundos para video de 27s)
                        try:
                            self.video_process.wait(timeout=30)
                            print(f"Video reproducido exitosamente con {cmd_base[0]}")
                            return True
                        except subprocess.TimeoutExpired:
                            # El video está tomando más tiempo, terminarlo
                            self.video_process.terminate()
                            try:
                                self.video_process.wait(timeout=2)
                            except subprocess.TimeoutExpired:
                                self.video_process.kill()
                            return True
                        
                except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                    continue
            
            # Si ningún reproductor funcionó, usar fallback
            print("No se encontró reproductor de video, usando fallback")
            self.reproducir_video_placeholder(video_file)
            return False
            
        except Exception as e:
            print(f"Error en reproducción de video Linux: {e}")
            self.reproducir_video_placeholder(video_file)
            return False
    
    def reproducir_video_con_opencv_y_audio(self, video_file):
        """Reproducir video con OpenCV para visual y reproductor externo para audio"""
        try:
            import cv2
            from PIL import Image, ImageTk
            
            # Iniciar reproductor de audio en paralelo (solo audio)
            try:
                if sys.platform == 'darwin':
                    # En macOS, usar afplay para solo audio
                    audio_cmd = ['afplay', video_file]
                elif sys.platform.startswith('linux'):
                    # En Linux, usar reproductor en background
                    audio_cmd = ['mpv', '--no-video', '--really-quiet', video_file]
                else:
                    audio_cmd = None
                
                if audio_cmd:
                    self.audio_process = subprocess.Popen(
                        audio_cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            except:
                self.audio_process = None
                
            # Mostrar video con OpenCV
            self.reproducir_video_con_opencv(video_file)
            
            # Esperar a que termine el audio (que debe durar lo mismo que el video)
            if hasattr(self, 'audio_process') and self.audio_process:
                try:
                    self.audio_process.wait(timeout=30)
                    print("✅ Audio terminó naturalmente")
                except subprocess.TimeoutExpired:
                    self.audio_process.terminate()
                    print("⏰ Audio timeout, terminando proceso")
            
        except Exception as e:
            print(f"Error en reproducción combinada: {e}")
            self.reproducir_video_placeholder(video_file)
    
    def reproducir_video_placeholder(self, video_file):
        """Reproducir una animación placeholder cuando no hay OpenCV"""
        frames_placeholder = [
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n●○○○○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○●○○○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○○●○○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○○○●○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○○○○●",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○○○●○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○○●○○",
            "🎬\n\nREPRODUCIENDO VIDEO\n\nINSTRUCCIONES NODO 2\n\n○●○○○"
        ]
        
        # Reproducir el video externo con audio mientras mostramos la animación
        try:
            if sys.platform == 'darwin':
                cmd = ['open', video_file]
            elif sys.platform.startswith('linux'):
                # En Linux/Raspberry Pi, intentar reproductores con audio
                reproductores = [
                    ['omxplayer', '--no-osd', video_file],
                    ['vlc', '--play-and-exit', '--intf', 'dummy', video_file],
                    ['mpv', '--really-quiet', video_file],
                    ['mplayer', '-quiet', video_file]
                ]
                
                for cmd in reproductores:
                    try:
                        # Verificar si el comando existe
                        result = subprocess.run(['which', cmd[0]], 
                                              capture_output=True, 
                                              timeout=1)
                        if result.returncode == 0:
                            break
                    except:
                        continue
                else:
                    cmd = ['xdg-open', video_file]  # Fallback genérico
            else:
                cmd = ['start', video_file]
                
            self.video_process = subprocess.Popen(cmd, 
                                                 stdout=subprocess.DEVNULL, 
                                                 stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error al iniciar reproductor externo: {e}")
        
        # Mostrar animación en el área de video y esperar a que termine el video
        frame_actual = 0
        self.animacion_activa = True
        frames_por_segundo = 8
        delay_frame = 1000 // frames_por_segundo  # ~125ms por frame
        
        def animar_placeholder():
            nonlocal frame_actual
            
            if self.animacion_activa:
                # Mostrar frame actual
                texto_frame = frames_placeholder[frame_actual % len(frames_placeholder)]
                self.video_label.configure(text=texto_frame, fg='#00ff88', image="")
                
                frame_actual += 1
                self.root.after(delay_frame, animar_placeholder)
        
        # Iniciar animación
        animar_placeholder()
        
        # Esperar a que termine el proceso de video (27 segundos + margen)
        if hasattr(self, 'video_process') and self.video_process:
            try:
                self.video_process.wait(timeout=30)
                print("✅ Video externo terminó naturalmente")
            except subprocess.TimeoutExpired:
                self.video_process.terminate()
                print("⏰ Video externo timeout, terminando proceso")
        
        # Detener animación
        self.animacion_activa = False
    
    def detener_animacion_placeholder(self):
        """Detener la animación placeholder"""
        self.animacion_activa = False
    
    def reproducir_video_con_opencv(self, video_file):
        """Reproducir video usando OpenCV integrado en tkinter"""
        try:
            import cv2
            from PIL import Image, ImageTk
        except ImportError:
            raise ImportError("OpenCV o PIL no disponibles")
        
        # Abrir el video
        cap = cv2.VideoCapture(video_file)
        
        if not cap.isOpened():
            raise Exception("No se pudo abrir el video")
        
        # Obtener propiedades del video
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = int(1000 / fps)  # Delay en milisegundos
        
        def mostrar_frame():
            ret, frame = cap.read()
            
            if ret:
                # Redimensionar frame para ajustarse al área de video
                height, width = frame.shape[:2]
                
                # Forzar actualización del frame para obtener dimensiones reales
                self.video_frame.update_idletasks()
                area_width = self.video_frame.winfo_width()
                area_height = self.video_frame.winfo_height()
                
                # Usar dimensiones mínimas si el frame aún no está renderizado
                if area_width <= 1:
                    area_width = 800
                if area_height <= 1:
                    area_height = 600
                
                # Calcular nuevo tamaño manteniendo aspecto
                scale_w = area_width / width
                scale_h = area_height / height
                scale = min(scale_w, scale_h) * 0.8  # 80% del área disponible
                
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                if new_width > 0 and new_height > 0:
                    frame_resized = cv2.resize(frame, (new_width, new_height))
                    
                    # Convertir de BGR a RGB
                    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    
                    # Convertir a formato PIL
                    pil_image = Image.fromarray(frame_rgb)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Actualizar el label con la imagen
                    self.video_label.configure(image=photo, text="")
                    self.video_label.image = photo  # Mantener referencia
                
                # Programar siguiente frame
                self.root.after(frame_delay, mostrar_frame)
            else:
                # Video terminado
                cap.release()
        
        # Iniciar reproducción
        self.root.after(500, mostrar_frame)  # Delay inicial más largo
    
    def reproducir_video_externo(self, video_file):
        """Fallback: reproducir video en ventana externa"""
        try:
            if sys.platform == 'darwin':
                # En macOS, intentar usar QuickTime Player en modo específico
                cmd = ['open', '-a', 'QuickTime Player', video_file]
            elif sys.platform.startswith('linux'):
                # En Linux, usar vlc si está disponible
                cmd = ['vlc', '--intf', 'dummy', '--play-and-exit', video_file]
            else:
                # En Windows
                cmd = ['start', video_file]
                
            self.video_process = subprocess.Popen(cmd, 
                                                 stdout=subprocess.DEVNULL, 
                                                 stderr=subprocess.DEVNULL)
            
            self.mostrar_video_en_area(True, "🎬\n\nVIDEO REPRODUCIÉNDOSE\n\nen ventana externa")
            
            # Esperar a que termine el video o timeout
            try:
                self.video_process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.video_process.terminate()
                
        except Exception as e:
            pass
            
    def limpiar_procesos_multimedia(self):
        """Limpiar procesos de audio y video que puedan estar corriendo"""
        try:
            # Terminar proceso de video si existe
            if hasattr(self, 'video_process') and self.video_process:
                try:
                    self.video_process.terminate()
                    self.video_process.wait(timeout=2)
                except (subprocess.TimeoutExpired, ProcessLookupError):
                    try:
                        self.video_process.kill()
                    except:
                        pass
                finally:
                    self.video_process = None
            
            # Terminar proceso de audio si existe
            if hasattr(self, 'audio_process') and self.audio_process:
                try:
                    self.audio_process.terminate()
                    self.audio_process.wait(timeout=2)
                except (subprocess.TimeoutExpired, ProcessLookupError):
                    try:
                        self.audio_process.kill()
                    except:
                        pass
                finally:
                    self.audio_process = None
                    
        except Exception as e:
            pass  # Limpieza silenciosa
            
    def grabar_voz_con_visual(self):
        """Grabar voz con indicador visual en tiempo real"""
        
        # Ejecutar grabación real usando la nueva lógica
        archivo = self.logica_clonacion.grabar_voz()
        return archivo
            
    def salir_aplicacion(self):
        """Cerrar la aplicación con confirmación"""
        if self.proceso_activo:
            messagebox.showwarning(
                "Proceso Activo", 
                "Hay una experiencia en progreso. Espera a que termine antes de salir."
            )
            return
        
        # Limpiar procesos multimedia antes de salir
        self.limpiar_procesos_multimedia()
            
        # En fullscreen, salir directamente sin confirmación
        self.root.quit()
            
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    
    # Verificar dependencias básicas
    try:
        import pyaudio
        import requests
    except ImportError as e:
        return
        
    # Iniciar aplicación
    app = ExperienciaVozApp()
    app.run()

if __name__ == "__main__":
    main()
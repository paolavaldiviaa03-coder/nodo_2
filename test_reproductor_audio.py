#!/usr/bin/env python3
"""
Prueba rápida del reproductor de audio sin interfaz visual
"""

import subprocess
import sys
import time

def probar_reproductor_audio():
    """Probar que el reproductor de audio funcione sin ventanas emergentes"""
    video_file = 'instrucciones.mp4'
    
    print("🧪 PROBANDO REPRODUCTOR DE AUDIO SIN VENTANAS")
    print("=" * 50)
    
    if sys.platform == 'darwin':
        cmd = ['afplay', video_file]
        print("🍎 macOS: Usando afplay (solo audio)")
    elif sys.platform.startswith('linux'):
        # Intentar reproductores en orden
        reproductores = [
            ['vlc', '--intf', 'dummy', '--play-and-exit', '--no-video', video_file],
            ['mpv', '--really-quiet', '--no-video', video_file],
            ['mplayer', '-quiet', '-novideo', video_file]
        ]
        
        for cmd in reproductores:
            try:
                result = subprocess.run(['which', cmd[0]], 
                                      capture_output=True, 
                                      timeout=1)
                if result.returncode == 0:
                    print(f"🐧 Linux: Usando {cmd[0]} (solo audio)")
                    break
            except:
                continue
        else:
            print("❌ No se encontró reproductor compatible")
            return False
    else:
        print("🪟 Windows: Función no implementada para esta prueba")
        return False
    
    try:
        print(f"▶️ Ejecutando: {' '.join(cmd)}")
        print("📢 Deberías escuchar audio SIN que aparezca ventana de video")
        print("⏰ El audio durará ~27 segundos")
        
        # Ejecutar reproductor
        process = subprocess.Popen(cmd, 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        
        # Esperar 5 segundos para verificar
        print("⏱️ Esperando 5 segundos para verificar...")
        time.sleep(5)
        
        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            print("✅ Proceso corriendo correctamente")
            print("🔊 Si escuchas audio SIN ventana = ¡PERFECTO!")
            
            # Terminar el proceso para no seguir reproduciendo
            process.terminate()
            process.wait(timeout=2)
            print("⏹️ Proceso terminado")
            return True
        else:
            print("❌ El proceso terminó prematuramente")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Esta prueba verifica que el audio se reproduzca sin ventanas emergentes")
    print("que puedan interferir con la interfaz de la aplicación.\n")
    
    success = probar_reproductor_audio()
    
    if success:
        print("\n🎉 ¡PERFECTO! El reproductor funciona sin interferir con la interfaz")
    else:
        print("\n❌ Hay problemas con el reproductor. Revisa la configuración.")
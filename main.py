#!/usr/bin/env python3
"""
MAIN - EXPERIENCIA NODO 2
========================
Aplicación principal que integra la interfaz gráfica 
con la lógica de clonación de voz.

Estructura del proyecto:
- main.py: Archivo principal (este archivo)
- interfaz_experiencia.py: Interfaz gráfica fullscreen
- logica_clonacion.py: Lógica de clonación con ElevenLabs
- test_audio.py: Utilidad para probar audio
- check_raspberry_pi.sh: Verificación para Raspberry Pi OS
"""

import sys
import os
from pathlib import Path

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    dependencias_faltantes = []
    
    try:
        import tkinter
    except ImportError:
        dependencias_faltantes.append("tkinter")
    
    try:
        import pyaudio
    except ImportError:
        dependencias_faltantes.append("pyaudio")
    
    try:
        import requests
    except ImportError:
        dependencias_faltantes.append("requests")
    
    try:
        import PIL
    except ImportError:
        dependencias_faltantes.append("pillow")
    
    if dependencias_faltantes:
        print("❌ DEPENDENCIAS FALTANTES:")
        for dep in dependencias_faltantes:
            print(f"   • {dep}")
        print("\nInstala las dependencias con:")
        print("pip install pyaudio requests pillow")
        if "tkinter" in dependencias_faltantes:
            print("sudo apt-get install python3-tk  # En Linux")
        return False
    
    return True

def verificar_archivos():
    """Verificar que todos los archivos necesarios existan"""
    archivos_necesarios = [
        "interfaz_experiencia.py",
        "logica_clonacion.py",
        "instrucciones.mp4"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print("❌ ARCHIVOS FALTANTES:")
        for archivo in archivos_faltantes:
            print(f"   • {archivo}")
        return False
    
    return True

def mostrar_informacion_sistema():
    """Mostrar información del sistema"""
    print("🖥️  INFORMACIÓN DEL SISTEMA:")
    print(f"   • Sistema operativo: {sys.platform}")
    print(f"   • Versión de Python: {sys.version.split()[0]}")
    print(f"   • Directorio de trabajo: {os.getcwd()}")
    
    # Información específica para Raspberry Pi
    if sys.platform.startswith('linux'):
        try:
            with open('/proc/cpuinfo', 'r') as f:
                if 'Raspberry Pi' in f.read():
                    print("   • 🍓 Raspberry Pi detectado")
                else:
                    print("   • 🐧 Sistema Linux genérico")
        except:
            print("   • 🐧 Sistema Linux")
    elif sys.platform == 'darwin':
        print("   • 🍎 macOS")
    elif sys.platform.startswith('win'):
        print("   • 🪟 Windows")

def main():
    """Función principal"""
    print("=" * 70)
    print("      🎤 EXPERIENCIA NODO 2 - CLONACIÓN DE VOZ")
    print("=" * 70)
    
    # Verificaciones previas
    print("\n🔍 VERIFICANDO SISTEMA...")
    mostrar_informacion_sistema()
    
    print("\n📋 VERIFICANDO DEPENDENCIAS...")
    if not verificar_dependencias():
        print("\n❌ No se puede continuar sin las dependencias necesarias.")
        sys.exit(1)
    print("✅ Todas las dependencias están disponibles")
    
    print("\n📁 VERIFICANDO ARCHIVOS...")
    if not verificar_archivos():
        print("\n❌ No se puede continuar sin los archivos necesarios.")
        sys.exit(1)
    print("✅ Todos los archivos necesarios están presentes")
    
    # Importar y ejecutar la aplicación
    try:
        print("\n🚀 INICIANDO APLICACIÓN...")
        
        # Agregar el directorio actual al path
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Importar la aplicación de interfaz
        from interfaz_experiencia import ExperienciaVozApp
        
        print("✅ Módulos importados correctamente")
        print("\n" + "=" * 70)
        print("    INSTRUCCIONES:")
        print("    • La aplicación se abrirá en pantalla completa")
        print("    • Presiona ESCAPE para salir")
        print("    • Asegúrate de que tu micrófono esté funcionando")
        print("    • Ten altavoces o audífonos conectados")
        print("=" * 70)
        
        # Crear y ejecutar la aplicación
        app = ExperienciaVozApp()
        app.run()
        
    except ImportError as e:
        print(f"\n❌ Error al importar módulos: {e}")
        print("Verifica que todos los archivos estén en el directorio correcto.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Aplicación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n👋 ¡Gracias por usar la Experiencia Nodo 2!")

if __name__ == "__main__":
    main()
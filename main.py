#!/usr/bin/env python3
# =====================================================
# LANZADOR PRINCIPAL - EXPERIENCIA DE CLONACIÓN DE VOZ
# =====================================================
# Archivo principal para ejecutar la experiencia

import sys
import os

def main():
    """Lanzar la aplicación de experiencia de voz"""
    print("🎤 Nodo 2 - Experiencia de Clonación de Voz")
    print("=" * 50)
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return
        
    # Verificar archivos necesarios
    archivos_requeridos = [
        'interfaz_experiencia.py',
        'voice_cloner.py',
        'instrucciones.mp4'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
            
    if archivos_faltantes:
        print("❌ Error: Archivos faltantes:")
        for archivo in archivos_faltantes:
            print(f"   - {archivo}")
        print("\nAsegúrate de tener todos los archivos en el mismo directorio")
        return
        
    # Verificar dependencias básicas
    try:
        import pyaudio
        print("✅ PyAudio encontrado")
    except ImportError:
        print("❌ PyAudio no instalado. Ejecuta: pip install pyaudio")
        return
        
    try:
        import requests
        print("✅ Requests encontrado")
    except ImportError:
        print("❌ Requests no instalado. Ejecuta: pip install requests")
        return
        
    try:
        import tkinter
        print("✅ Tkinter encontrado")
    except ImportError:
        print("❌ Tkinter no disponible. Instala python3-tk en tu sistema")
        return
        
    print("✅ Todas las dependencias están disponibles")
    print("\n🚀 Iniciando interfaz gráfica...")
    
    # Importar y ejecutar interfaz
    try:
        from interfaz_experiencia import main as run_interface
        run_interface()
    except Exception as e:
        print(f"❌ Error al iniciar la interfaz: {e}")
        print("\nIntentando modo consola...")
        
        # Fallback: modo consola
        try:
            from voice_cloner import VoiceCloner
            cloner = VoiceCloner()
            cloner.ejecutar_experiencia_completa()
        except Exception as e2:
            print(f"❌ Error en modo consola: {e2}")

if __name__ == "__main__":
    main()
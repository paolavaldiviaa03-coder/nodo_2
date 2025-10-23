#!/usr/bin/env python3
# =====================================================
# TEST RÁPIDO - Verificación del Sistema
# =====================================================
# Script para verificar que todo funciona correctamente

import sys
import os

def test_python_version():
    """Verificar versión de Python"""
    print(f"🐍 Python: {sys.version}")
    if sys.version_info >= (3, 7):
        print("   ✅ Versión compatible")
        return True
    else:
        print("   ❌ Se requiere Python 3.7+")
        return False

def test_imports():
    """Verificar imports necesarios"""
    print("\n📦 Verificando dependencias...")
    
    imports_ok = True
    
    # PyAudio
    try:
        import pyaudio
        print("   ✅ PyAudio disponible")
    except ImportError:
        print("   ❌ PyAudio NO disponible")
        imports_ok = False
        
    # Requests
    try:
        import requests
        print("   ✅ Requests disponible")
    except ImportError:
        print("   ❌ Requests NO disponible")
        imports_ok = False
        
    # Tkinter
    try:
        import tkinter
        print("   ✅ Tkinter disponible")
    except ImportError:
        print("   ❌ Tkinter NO disponible")
        imports_ok = False
        
    return imports_ok

def test_audio_devices():
    """Verificar dispositivos de audio"""
    print("\n🎤 Verificando dispositivos de audio...")
    
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        input_devices = 0
        output_devices = 0
        
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices += 1
            if info['maxOutputChannels'] > 0:
                output_devices += 1
                
        p.terminate()
        
        print(f"   🎙️ Dispositivos de entrada: {input_devices}")
        print(f"   🔊 Dispositivos de salida: {output_devices}")
        
        if input_devices > 0 and output_devices > 0:
            print("   ✅ Audio configurado correctamente")
            return True
        else:
            print("   ❌ Faltan dispositivos de audio")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando audio: {e}")
        return False

def test_files():
    """Verificar archivos necesarios"""
    print("\n📁 Verificando archivos...")
    
    files_required = [
        ('main.py', '🚀 Lanzador principal'),
        ('interfaz_experiencia.py', '🖥️ Interfaz gráfica'),
        ('voice_cloner.py', '🤖 Lógica de clonación'),
        ('instrucciones.mp4', '📹 Video de instrucciones'),
        ('requirements.txt', '📦 Dependencias')
    ]
    
    all_ok = True
    
    for filename, description in files_required:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {filename} - {description} ({size} bytes)")
        else:
            print(f"   ❌ {filename} - {description} (FALTANTE)")
            all_ok = False
            
    return all_ok

def test_internet():
    """Verificar conexión a internet"""
    print("\n🌐 Verificando conexión a internet...")
    
    try:
        import requests
        response = requests.get('https://api.elevenlabs.io/v1/voices', timeout=5)
        if response.status_code in [200, 401]:  # 401 es OK (sin API key)
            print("   ✅ Conexión a ElevenLabs OK")
            return True
        else:
            print(f"   ⚠️ ElevenLabs responde con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def show_summary(results):
    """Mostrar resumen final"""
    print("\n" + "="*50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        
    print(f"\nResultado: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODO LISTO! Puedes ejecutar:")
        print("   python main.py")
    else:
        print(f"\n⚠️ Hay {total_tests - passed_tests} problemas que resolver")
        print("   Consulta README.md para soluciones")

def main():
    """Ejecutar todas las pruebas"""
    print("🔍 VERIFICACIÓN DEL SISTEMA - NODO 2")
    print("="*50)
    
    results = {
        'Versión de Python': test_python_version(),
        'Dependencias Python': test_imports(),
        'Dispositivos de Audio': test_audio_devices(),
        'Archivos del Proyecto': test_files(),
        'Conexión a Internet': test_internet()
    }
    
    show_summary(results)

if __name__ == "__main__":
    main()
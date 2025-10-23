# =====================================================
# CLONADOR DE VOZ - ElevenLabs + PyAudio
# =====================================================
# Este script:
# 1. Abre un video de instrucciones
# 2. Graba audio del micrófono (30s)
# 3. Sube el audio a ElevenLabs para clonar la voz
# 4. Sintetiza una frase final usando la voz clonada
# 5. Limpia la voz temporal de ElevenLabs

import pyaudio
import wave
import time
import os
import sys
import subprocess
import requests

# =====================================================
# CONFIGURACIÓN
# =====================================================
API_KEY = "8007664948e8dd45023e33e533ca8c3782511d7d62913ee436b83bc36ea16746" 
TEXTO_FINAL = "Hola, esta es mi voz clonada usando inteligencia artificial. Como puedes escuchar, suena exactamente igual que cuando hablé durante la grabación. Es increíble cómo la tecnología puede replicar mi manera de hablar, mi tono y mi acento de forma tan precisa."
ARCHIVO_FINAL = "frase_final_clonada.mp3"
VIDEO_FILE = 'instrucciones.mp4'
FILENAME = "voz_sample.wav"
DURATION_SECONDS = 30  # Duración de la grabación
CHUNK = 1024           # Buffer de audio por iteración
FORMAT = pyaudio.paInt16 # Formato de 16 bits
CHANNELS = 1           # Grabar en mono
RATE = 44100           # Frecuencia de muestreo (44.1 kHz)

# Endpoints de ElevenLabs
URL_ADD_VOICE = "https://api.elevenlabs.io/v1/voices/add"
URL_TTS = "https://api.elevenlabs.io/v1/text-to-speech/" 
URL_DELETE_VOICE = "https://api.elevenlabs.io/v1/voices/"
URL_GET_VOICES = "https://api.elevenlabs.io/v1/voices"

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def abrir_archivo(path):
    """Abrir archivo multiplataforma: Windows (os.startfile), macOS (open), Linux (xdg-open)."""
    if sys.platform.startswith('win'):
        return os.startfile(path)
    elif sys.platform == 'darwin':
        return subprocess.Popen(['open', path])
    else:
        # Linux/Unix
        return subprocess.Popen(['xdg-open', path])


def reproducir_video_instrucciones():
    """Abre el video de instrucciones si existe."""
    if not os.path.exists(VIDEO_FILE):
        print(f"Error: El archivo '{VIDEO_FILE}' no fue encontrado.")
        return False
    
    print(f"▶️ Abriendo: {VIDEO_FILE} con el reproductor predeterminado del sistema.")  
    try:
        abrir_archivo(VIDEO_FILE)
        time.sleep(2)  # Tiempo para que se inicie el reproductor
        print("Video reproduciéndose en ventana externa.")
        return True
    except Exception as e:
        print(f"Error al abrir el video: {e}")
        return False


def grabar_y_almacenar_voz(filename=FILENAME, duration=DURATION_SECONDS, input_device_index=None):
    """
    Graba audio del micrófono durante la duración especificada y guarda como WAV.
    
    Args:
        filename: Nombre del archivo de salida
        duration: Duración en segundos
        input_device_index: Índice del dispositivo de entrada (None = por defecto)
    
    Returns:
        str: Ruta del archivo guardado o None si falla
    """
    print("\n" + "="*60)
    print("INICIANDO GRABACIÓN DE AUDIO")
    print("="*60)
    
    # Inicializar PyAudio
    p = pyaudio.PyAudio()

    # Mostrar dispositivos disponibles si no se especifica índice
    if input_device_index is None:
        print("Dispositivos de audio disponibles:")
        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            if dev.get('maxInputChannels', 0) > 0:
                print(f"  Index {i}: {dev.get('name')}")
        print("Usando dispositivo por defecto. Para cambiar, especifica input_device_index\n")

    try:
        # Abrir stream de audio
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=CHUNK)
        
        print(f"🎤 GRABANDO por {duration} segundos...")
        print("Texto sugerido: 'Hola, soy yo, y estoy haciendo esta grabación para crear")
        print("mi voz digital. Me encanta cómo la tecnología puede capturar cada detalle,'")
        print("cada tono, y transformarlo en algo único. Espero que esta versión suene")
        print("tan natural y auténtica como yo.'")
        print("-" * 60)
        
        frames = []
        
        # Capturar datos del micrófono
        for i in range(0, int(RATE / CHUNK * duration)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except IOError as e:
                print(f"Error de lectura: {e}")
                continue
        
        print("-" * 60)
        print("✅ GRABACIÓN FINALIZADA. Guardando archivo...")
        
        # Cerrar stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Guardar como archivo WAV
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"💾 Audio guardado: {os.path.abspath(filename)}")
        return filename
        
    except Exception as e:
        print(f"❌ Error en la grabación: {e}")
        p.terminate()
        return None


def esperar_voz_lista(voice_id, timeout_segundos=120):
    """
    Espera a que la voz clonada esté lista consultando la lista de voces del usuario.
    
    Args:
        voice_id: ID de la voz clonada
        timeout_segundos: Tiempo máximo de espera
    
    Returns:
        bool: True si la voz está lista, False si timeout
    """
    headers = {"xi-api-key": API_KEY}
    waited = 0
    interval = 15
    
    print(f"[IA] Verificando que la voz {voice_id} esté procesada (timeout: {timeout_segundos}s)...")
    
    while waited < timeout_segundos:
        try:
            # Consultar la lista completa de voces del usuario
            response = requests.get(URL_GET_VOICES, headers=headers)
            
            if response.status_code == 200:
                voices_data = response.json()
                voices = voices_data.get('voices', [])
                
                # Buscar nuestra voz en la lista
                found_voice = None
                for voice in voices:
                    if voice.get('voice_id') == voice_id:
                        found_voice = voice
                        break
                
                if found_voice:
                    voice_name = found_voice.get('name', 'Unknown')
                    samples = found_voice.get('samples', [])
                    print(f"[IA] ✅ Voz '{voice_name}' encontrada con {len(samples)} muestras procesadas")
                    
                    # Si tiene muestras, está lista para usar
                    if samples:
                        print(f"[IA] 🎯 Voz lista para síntesis tras {waited}s")
                        return True
                    else:
                        print(f"[IA] ⏳ Voz encontrada pero sin muestras aún... esperando")
                else:
                    print(f"[IA] ⏳ Voz {voice_id} aún no aparece en la lista... ({waited}s)")
            else:
                print(f"[IA] ❌ Error consultando voces: {response.status_code}")
                
        except Exception as e:
            print(f"[IA] ❌ Error verificando voz: {e}")
        
        time.sleep(interval)
        waited += interval
    
    print(f"⚠️ Timeout alcanzado ({timeout_segundos}s). La voz podría no estar lista.")
    return False


def clonar_y_sintetizar_usuario(audio_sample_path, texto_a_sintetizar):
    """
    Flujo completo de clonación:
    1. Sube muestra de voz a ElevenLabs
    2. Espera a que se procese (opcional)
    3. Sintetiza texto usando la voz clonada
    4. Guarda el MP3 resultante
    
    Args:
        audio_sample_path: Ruta al archivo WAV de muestra
        texto_a_sintetizar: Texto a convertir con la voz clonada
    
    Returns:
        tuple: (archivo_mp3, voice_id) o (None, None) si falla
    """
    print("\n" + "="*60)
    print("INICIANDO CLONACIÓN DE VOZ")
    print("="*60)
    
    headers = {"xi-api-key": API_KEY}
    
    # ---- ETAPA 1: SUBIR MUESTRA DE VOZ ----
    print(f"📤 Subiendo muestra: {os.path.basename(audio_sample_path)}")
    
    data_upload = {
        'name': f'Temp_Voice_{int(time.time())}',
        'description': 'Voz temporal para prototipo',
        'labels': '{"source": "prototipo"}'
    }
    
    try:
        with open(audio_sample_path, 'rb') as audio_file:
            files = {'files': (os.path.basename(audio_sample_path), audio_file, 'audio/wav')}
            
            response_upload = requests.post(
                URL_ADD_VOICE, 
                headers=headers, 
                data=data_upload, 
                files=files
            )
            response_upload.raise_for_status()
        
        upload_json = response_upload.json()
        voice_id = upload_json.get('voice_id')
        
        if not voice_id:
            print(f"❌ No se obtuvo voice_id. Respuesta: {upload_json}")
            return None, None
            
        print(f"✅ Voz subida. ID: {voice_id}")
        
    except Exception as e:
        print(f"❌ Error subiendo voz: {e}")
        return None, None
    
    # ---- ETAPA 2: ESPERAR PROCESAMIENTO (CRÍTICO) ----
    print("⏳ ESPERANDO que ElevenLabs procese tu muestra de voz...")
    print("   Esto es CRÍTICO: sin esperar, ElevenLabs usará una voz genérica")
    voz_lista = esperar_voz_lista(voice_id, timeout_segundos=180)
    
    if not voz_lista:
        print("⚠️ WARNING: La voz podría no estar completamente procesada")
        print("   El resultado podría ser una voz genérica en lugar de la tuya")
    
    # ---- ETAPA 3: SINTETIZAR CON TU VOZ CLONADA ----
    print(f"🎵 SINTETIZANDO con TU voz clonada (ID: {voice_id})")
    print(f"   Texto a sintetizar: '{texto_a_sintetizar[:60]}...'")
    
    headers_synthesis = {
        "xi-api-key": API_KEY,
        "Accept": "audio/mpeg", 
        "Content-Type": "application/json"
    }
    
    data_synthesis = {
        "text": texto_a_sintetizar,
        "model_id": "eleven_multilingual_v2",  # Modelo multilingüe con mejor soporte para español
        "voice_settings": {
            "stability": 0.5,       # Estabilidad media para español
            "similarity_boost": 0.85, # Alta similitud a la muestra original
            "style": 0.1,           # Ligero estilo para naturalidad
            "use_speaker_boost": True
        },
        "pronunciation_dictionary_locators": [],  # Para futuras mejoras de pronunciación
        "seed": None,
        "previous_text": None,
        "next_text": None,
        "previous_request_ids": [],
        "next_request_ids": []
    }

    try:
        print(f"[DEBUG] Enviando petición de síntesis...")
        print(f"[DEBUG] URL: {URL_TTS}{voice_id}")
        print(f"[DEBUG] Voice settings: {data_synthesis['voice_settings']}")
        
        response_synthesis = requests.post(
            f"{URL_TTS}{voice_id}", 
            headers=headers_synthesis, 
            json=data_synthesis
        )
        
        print(f"[DEBUG] Respuesta HTTP: {response_synthesis.status_code}")
        
        if response_synthesis.status_code != 200:
            print(f"❌ ERROR HTTP {response_synthesis.status_code}")
            print(f"   Respuesta: {response_synthesis.text}")
            return None, voice_id
        
        response_synthesis.raise_for_status()
        
        # Análisis detallado de la respuesta
        content_size = len(response_synthesis.content)
        print(f"📦 Audio recibido: {content_size} bytes")
        
        # Verificaciones de calidad
        if content_size < 2000:
            print("❌ PROBLEMA GRAVE: Archivo demasiado pequeño!")
            print("   Esto indica que ElevenLabs NO usó tu voz clonada")
            print("   Posibles causas:")
            print("   • La voz aún se está procesando en el servidor")
            print("   • voice_id incorrecto o expirado")
            print("   • Audio de muestra rechazado por baja calidad")
            print("   • Límites de API alcanzados")
        elif content_size < 5000:
            print("⚠️ Archivo pequeño - podría ser voz genérica")
        else:
            print("✅ Tamaño correcto - probablemente es tu voz clonada")
        
        # Verificar headers de respuesta
        content_type = response_synthesis.headers.get('content-type', '')
        if 'audio' not in content_type.lower():
            print(f"⚠️ Content-Type inesperado: {content_type}")
        
        # Guardar el archivo
        with open(ARCHIVO_FINAL, 'wb') as f:
            f.write(response_synthesis.content)
            
        final_size = os.path.getsize(ARCHIVO_FINAL)
        print(f"✅ MP3 guardado: {ARCHIVO_FINAL} ({final_size} bytes)")
        
        return ARCHIVO_FINAL, voice_id
        
    except Exception as e:
        print(f"❌ Error en síntesis: {e}")
        if 'response_synthesis' in locals():
            print(f"   Response preview: {response_synthesis.content[:100] if response_synthesis.content else 'No content'}")
        return None, voice_id


def eliminar_voz_clonada(voice_id):
    """Elimina la voz temporal de ElevenLabs para evitar costos."""
    if not voice_id:
        return
    
    print(f"🧹 Limpiando voz temporal: {voice_id}")
    
    headers = {"xi-api-key": API_KEY}
    
    try:
        response = requests.delete(f"{URL_DELETE_VOICE}{voice_id}", headers=headers)
        response.raise_for_status()
        print("✅ Voz temporal eliminada")
    except Exception as e:
        print(f"⚠️ Error eliminando voz {voice_id}: {e}")
        print("   Elimínala manualmente desde console.elevenlabs.io")


# =====================================================
# FLUJO PRINCIPAL
# =====================================================
if __name__ == "__main__":
    print("="*70)
    print("       CLONADOR DE VOZ - ElevenLabs + PyAudio")
    print("="*70)
    print("Este programa:")
    print("1. 📹 Reproduce video de instrucciones")
    print("2. 🎤 Graba tu voz (30 segundos)")
    print("3. ☁️  Clona tu voz en ElevenLabs")
    print("4. 🎵 Sintetiza frase final con tu voz clonada")
    print("5. 🧹 Limpia recursos temporales")
    print("="*70)
    
    try:
        # PASO 1: Reproducir video de instrucciones
        print("\n📹 PASO 1: Video de instrucciones")
        video_ok = reproducir_video_instrucciones()
        if video_ok:
            input("Presiona ENTER cuando hayas visto el video y estés listo para grabar...")
        
        # PASO 2: Grabar audio
        print("\n🎤 PASO 2: Grabación de audio")
        archivo_audio = grabar_y_almacenar_voz()
        
        if not archivo_audio:
            print("❌ Error en la grabación. Abortando.")
            sys.exit(1)
        
        # PASO 3 y 4: Clonar voz y sintetizar
        print("\n☁️ PASO 3-4: Clonación y síntesis")
        archivo_mp3, voice_id = clonar_y_sintetizar_usuario(archivo_audio, TEXTO_FINAL)
        
        # PASO 5: Limpieza
        print("\n🧹 PASO 5: Limpieza")
        eliminar_voz_clonada(voice_id)
        
        # RESULTADO FINAL
        print("\n" + "="*70)
        if archivo_mp3 and os.path.exists(archivo_mp3):
            size_kb = os.path.getsize(archivo_mp3) / 1024
            print(f"🎉 ¡PROCESO COMPLETADO!")
            print(f"📁 Archivos generados:")
            print(f"   • Audio original grabado: {archivo_audio}")
            print(f"   • Tu voz clonada sintetizando texto: {archivo_mp3} ({size_kb:.1f} KB)")
            print(f"\n💡 Para reproducir el resultado:")
            print(f"   mpg123 '{archivo_mp3}'  # En Linux")
            print(f"   afplay '{archivo_mp3}'  # En macOS")
            print(f"\n🎯 QUE DEBERÍAS ESCUCHAR:")
            print(f"   El archivo MP3 debe contener tu PROPIA VOZ diciendo:")
            print(f"   '{TEXTO_FINAL[:80]}...'")
            print(f"   Si suena como tu voz → ✅ Clonación exitosa")
            print(f"   Si suena genérico → ❌ ElevenLabs usó voz por defecto")
            
            # Diagnóstico si el archivo es muy pequeño
            if size_kb < 10:
                print(f"\n⚠️  DIAGNÓSTICO: El archivo es muy pequeño ({size_kb:.1f} KB)")
                print("   PROBABLE CAUSA: ElevenLabs NO usó tu voz clonada")
                print("   Razones comunes:")
                print("   • El audio grabado fue muy corto o silencioso")
                print("   • La voz no terminó de procesarse en ElevenLabs")
                print("   • Problemas con la calidad del micrófono")
                print("   • Límites de la cuenta de ElevenLabs alcanzados")
                print("\n💡 Soluciones:")
                print("   • Graba nuevamente hablando MÁS FUERTE y CLARO")
                print("   • Asegúrate de hablar durante TODOS los 30 segundos")
                print("   • Verifica tu cuenta en console.elevenlabs.io")
                print("   • Usa un micrófono de mejor calidad")
            elif size_kb > 30:
                print(f"\n✅ Tamaño bueno ({size_kb:.1f} KB) - probablemente tu voz clonada")
        else:
            print("❌ Error: No se pudo completar el proceso")
        
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

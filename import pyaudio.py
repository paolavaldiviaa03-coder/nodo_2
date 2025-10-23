import pyaudio
import wave
import time
import os
import sys
import subprocess
import requests

API_KEY = "8007664948e8dd45023e33e533ca8c3782511d7d62913ee436b83bc36ea16746" 
URL_BASE_API = "https://elevenlabs.io/app/voice-lab" 
TEXTO_FINAL = "Gracias por regalarnos tu voz."
ARCHIVO_FINAL = "frase_final_clonada.mp3"
VIDEO_FILE = 'instrucciones.mp4' 
if not os.path.exists(VIDEO_FILE):
    print(f"Error: El archivo '{VIDEO_FILE}' no fue encontrado.")
else:
    print(f"▶️ Abriendo: {VIDEO_FILE} con el reproductor predeterminado del sistema.")  
    try:
        # Abrir el archivo con la aplicación por defecto de forma multiplataforma.
        def abrir_archivo(path):
            """Abrir archivo en el sistema: Windows uses os.startfile, macOS uses `open`, Linux uses `xdg-open`."""
            if sys.platform.startswith('win'):
                return os.startfile(path)
            elif sys.platform == 'darwin':
                return subprocess.Popen(['open', path])
            else:
                # Asumimos Linux/Unix
                return subprocess.Popen(['xdg-open', path])

        abrir_archivo(VIDEO_FILE)
        # Le da tiempo al reproductor para que se inicie
        time.sleep(2)
        print("El script de Python ha terminado. El video se está reproduciendo en una ventana externa.")
    except Exception as e:
        print(f"Ocurrió un error al intentar abrir el archivo: {e}")
FILENAME = "voz_sample.wav"
DURATION_SECONDS = 30  # Duración de la grabación (para las frases)
CHUNK = 1024           # Buffer de audio por iteración
FORMAT = pyaudio.paInt16 # Formato de 16 bits (calidad estándar)
CHANNELS = 1           # Grabar en mono
RATE = 44100           # Frecuencia de muestreo (44.1 kHz, estándar de CD)

def grabar_y_almacenar_voz(filename=FILENAME, duration=DURATION_SECONDS, input_device_index=None):
    """
    Función que inicializa el micrófono, graba durante la duración especificada 
    y guarda el audio en un archivo WAV.
    """
    # Inicializa PyAudio
    p = pyaudio.PyAudio()

    # Si no se especifica device index, listar dispositivos para ayudar al usuario (útil en Raspberry Pi)
    if input_device_index is None:
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        print("Dispositivos de audio disponibles:")
        for i in range(0, numdevices):
            dev = p.get_device_info_by_host_api_device_index(0, i)
            if dev.get('maxInputChannels') > 0:
                print(f"  Index {i}: {dev.get('name')}")
        print("Si el micrófono no está en el index por defecto, vuelva a ejecutar la función pasando input_device_index=<numero>\n")

    # Abrir el stream de audio para la entrada (micrófono)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=CHUNK)
    
    print("-" * 50)
    print(f"🎤 INICIANDO GRABACIÓN: Duración: {duration} segundos.")
    print("Por favor, repite las frases ahora: Hola, soy yo, y estoy haciendo esta grabación para crear mi voz digital. Me encanta cómo la tecnología puede capturar cada detalle, cada tono, y transformarlo en algo único. Espero que esta versión suene tan natural y auténtica como yo")
    print("-" * 50)
    
    frames = []
    
    # Captura los datos del micrófono
    # El bucle itera el número de veces necesario para alcanzar la DURACION_SECONDS
    for i in range(0, int(RATE / CHUNK * duration)):
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except IOError as e:
            # Manejo básico de errores de overflow (si la PC es lenta)
            print(f"Error de lectura de stream: {e}")
            pass
    
    print("-" * 50)
    print("✅ GRABACIÓN FINALIZADA. Guardando archivo...")
    print("-" * 50)
    
    # Detiene y cierra el stream de audio
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # --- 2. ALMACENAR LA VOZ (Guardar como archivo WAV) ---
    try:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"💾 Éxito: La voz se ha guardado en: {os.path.abspath(filename)}")
        return filename
    
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")
        return None

# --- Ejecución principal ---
if __name__ == "__main__":
    # Llama a la función para ejecutar la grabación
    ruta_archivo = grabar_y_almacenar_voz()

    if ruta_archivo:
        print(f"El archivo '{os.path.basename(ruta_archivo)}' está listo para la clonación de voz.")

import requests
import os
import time

# =======================================================
# --- 1. CONFIGURACIÓN DE TU API (REQUIERE CAMBIOS) ---
# =======================================================

# ⚠️ CAMBIO 1: Reemplaza con tu clave API REAL.
API_KEY = "8007664948e8dd45023e33e533ca8c3782511d7d62913ee436b83bc36ea16746" 
TEXTO_FINAL = "Gracias por regalarnos tu voz."
ARCHIVO_FINAL = "frase_final_clonada.mp3"

# Endpoints de ElevenLabs necesarios
URL_ADD_VOICE = "https://api.elevenlabs.io/v1/voices/add"
URL_TTS = "https://api.elevenlabs.io/v1/text-to-speech/" 
URL_DELETE_VOICE = "https://api.elevenlabs.io/v1/voices/" 


# =======================================================
# --- 2. FUNCIÓN DE CLONACIÓN ÚNICA POR USUARIO ---
# =======================================================

def clonar_y_sintetizar_usuario(audio_sample_path, texto_a_sintetizar):
    """
    Sube un nuevo archivo de voz, espera que se procese, sintetiza el texto
    y finalmente elimina la voz clonada.
    """
    # -----------------------------------------------------------------
    # ETAPA 1: SUBIR MUESTRA DE VOZ Y CREAR UN NUEVO VOICE ID ÚNICO
    # -----------------------------------------------------------------
    print(f"\n[IA] Iniciando Clonación de Voz. Subiendo {os.path.basename(audio_sample_path)}...")
    
    headers_upload = {
        "xi-api-key": API_KEY,
    }
    
    # Datos que acompañan el archivo
    data_upload = {
        'name': f'Temp_User_Voice_{int(time.time())}', # Nombre único para la voz temporal
        'description': 'Voz creada para un solo uso en un prototipo.',
        'labels': '{"accent": "prototipo"}'
    }
    
    # Adjuntar el archivo de audio
    files = {
        'files': (os.path.basename(audio_sample_path), open(audio_sample_path, 'rb'), 'audio/wav')
    }
    
    try:
        response_upload = requests.post(
            URL_ADD_VOICE, 
            headers=headers_upload, 
            data=data_upload, 
            files=files
        )
        response_upload.raise_for_status()

        upload_json = response_upload.json()
        print(f"[IA] Response upload: {upload_json}")

        voice_id_temporal = upload_json.get('voice_id') or upload_json.get('id')
        if not voice_id_temporal:
            print("⚠️ No se obtuvo voice_id tras la subida. Respuesta completa:", upload_json)
            return None, None

        print(f"[IA] Voz subida. ID Temporal creado: {voice_id_temporal}")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR al subir la voz: {e}")
        return None, None # Devolvemos None si falla
    
    # -----------------------------------------------------------------
    # ETAPA 2: ESPERAR LA SÍNTESIS Y SINTETIZAR LA FRASE FINAL
    # -----------------------------------------------------------------
    # NOTA: En la práctica real, aquí se pondría un bucle para verificar que 
    # el modelo de voz esté 'ready'. Por simplicidad de código, confiamos 
    # en que un plan profesional lo haga rápido o manejaremos el error.
    
    print("[IA] Sintetizando la frase final (puede tardar por el entrenamiento)...")
    
    headers_synthesis = {
        "xi-api-key": API_KEY,
        "Accept": "audio/mpeg", 
        "Content-Type": "application/json"
    }
    
    data_synthesis = {
        "text": texto_a_sintetizar,
        "model_id": "eleven_monolingual_v1", # Modelo TTS que uses
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    # Polling: verificar que la voz esté lista antes de pedir síntesis (timeout)
    check_url = f"{URL_DELETE_VOICE}{voice_id_temporal}"
    ready = False
    max_wait = 60  # segundos
    waited = 0
    interval = 5
    print(f"[IA] Esperando a que la voz clonada ({voice_id_temporal}) esté lista (timeout {max_wait}s)...")
    while waited < max_wait:
        try:
            r_check = requests.get(check_url, headers=headers_upload)
            if r_check.status_code == 200:
                info = r_check.json()
                # Intentar detectar un campo que indique readiness
                state = info.get('status') or info.get('state') or info.get('voice_state')
                print(f"[IA] Estado voice check: {state}")
                if state and str(state).lower() in ('ready', 'processed', 'available'):
                    ready = True
                    break
            else:
                print(f"[IA] check returned {r_check.status_code}: {r_check.text}")
        except Exception as e:
            print(f"[IA] Error consultando estado de la voz: {e}")

        time.sleep(interval)
        waited += interval

    if not ready:
        print("⚠️ Tiempo de espera excedido o voz no lista. Intentaremos la síntesis de todas formas (puede fallar o producir audio corto).")

    try:
        response_synthesis = requests.post(
            f"{URL_TTS}{voice_id_temporal}", 
            headers=headers_synthesis, 
            json=data_synthesis
        )
        response_synthesis.raise_for_status()

        # Verificar contenido mínimo antes de escribir
        if len(response_synthesis.content) < 2000:
            print(f"⚠️ Atención: El MP3 recibido es muy pequeño ({len(response_synthesis.content)} bytes). Podría ser solo una frase corta o un archivo inválido.")

        # Guardar el archivo de audio recibido (el MP3)
        with open(ARCHIVO_FINAL, 'wb') as f:
            f.write(response_synthesis.content)

        print(f"✅ Éxito IA: Frase clonada guardada como {ARCHIVO_FINAL} (tamaño {os.path.getsize(ARCHIVO_FINAL)} bytes)")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR al sintetizar la frase. El modelo podría no estar listo. {e}")
        # Asegúrate de eliminar la voz aunque la síntesis falle
        return ARCHIVO_FINAL, voice_id_temporal # Devolvemos el ID para la limpieza
    
    return ARCHIVO_FINAL, voice_id_temporal


# -----------------------------------------------------------------
# ETAPA 3: FUNCIÓN DE LIMPIEZA (CRUCIAL PARA LA GESTIÓN DE COSTOS)
# -----------------------------------------------------------------
def eliminar_voz_clonada(voice_id):
    """Elimina el Voice ID temporal creado para el usuario."""
    if not voice_id:
        return

    headers = {"xi-api-key": API_KEY}
    
    try:
        response = requests.delete(
            f"{URL_DELETE_VOICE}{voice_id}", 
            headers=headers
        )
        response.raise_for_status()
        print(f"[IA] Limpieza completada. Voice ID {voice_id} eliminado.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ ADVERTENCIA: No se pudo eliminar la voz {voice_id}. Por favor, elimínala manualmente.")
        print(e)


# =======================================================
# --- 4. FLUJO PRINCIPAL Y ORQUESTACIÓN (Ejemplo) ---
# =======================================================
if __name__ == "__main__":
    
    # 1. Ejecutar la función de grabación de voz (voz_sample.wav debe existir)
    # archivo_grabado = grabar_y_almacenar_voz(duration=30) # ¡Asegúrate de grabar 30s!
    
    # SIMULACIÓN DE ARCHIVO (asume que existe)
    ARCHIVO_DE_MUESTRA = "voz_sample.wav" 
    
    if os.path.exists(ARCHIVO_DE_MUESTRA):
        print("Iniciando flujo de clonación única de usuario...")
        
        # Inicia el procesamiento y obtén el Voice ID temporal
        archivo_clonado, voice_id_temporal = clonar_y_sintetizar_usuario(
            ARCHIVO_DE_MUESTRA, 
            TEXTO_FINAL
        )
        
        if archivo_clonado and voice_id_temporal:
            print("\n🎉 ¡Proceso de Clonación Completado!")
            # ------------------------------------------------------
            # AQUÍ VA LA REPRODUCCIÓN (Pygame) Y EL CIERRE (pyserial)
            # ------------------------------------------------------
        
        # ⚠️ Paso de Limpieza: Ejecutar SIEMPRE al final
        eliminar_voz_clonada(voice_id_temporal)
        
    else:
        print(f"ERROR: El archivo de muestra '{ARCHIVO_DE_MUESTRA}' no existe. Ejecuta la grabación primero.")

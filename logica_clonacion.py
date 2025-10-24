#!/usr/bin/env python3
"""
LÓGICA DE CLONACIÓN DE VOZ
========================
Módulo que maneja toda la lógica de clonación de voz usando ElevenLabs API.
Basado en la lógica original del archivo 'import pyaudio.py'
"""

import pyaudio
import wave
import time
import os
import sys
import subprocess
import requests

class LogicaClonacion:
    """Clase que maneja toda la lógica de clonación de voz"""
    
    def __init__(self):
        # Configuración
        self.API_KEY = "757588ed5afa48fbd81af949f67b2757655188c48b5057df968457741d7188fd"
        self.TEXTO_FINAL = "Gracias por regalarnos tu voz, ahora tengo el poder de hablar como tú, usarla para los fines que quiera, porque ahora es propiedad de nodo 2."
        self.ARCHIVO_FINAL = "frase_final_clonada.mp3"
        self.FILENAME = "voz_sample.wav"
        
        # Configuración de audio
        self.DURATION_SECONDS = 13
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        
        # URLs de ElevenLabs
        self.URL_ADD_VOICE = "https://api.elevenlabs.io/v1/voices/add"
        self.URL_TTS = "https://api.elevenlabs.io/v1/text-to-speech/"
        self.URL_DELETE_VOICE = "https://api.elevenlabs.io/v1/voices/"
        self.URL_GET_VOICES = "https://api.elevenlabs.io/v1/voices"
    
    def abrir_archivo(self, path):
        """Abrir archivo multiplataforma"""
        try:
            if sys.platform.startswith('win'):
                return os.startfile(path)
            elif sys.platform == 'darwin':
                return subprocess.Popen(['open', path])
            else:
                # Linux/Unix
                return subprocess.Popen(['xdg-open', path])
        except Exception as e:
            print(f"Error al abrir archivo {path}: {e}")
            return None
    
    def reproducir_solo_audio(self, archivo_audio):
        """Reproducir audio sin mostrar ventana (solo para archivos de audio)"""
        try:
            if sys.platform == 'darwin':
                # En macOS, usar afplay para solo audio
                cmd = ['afplay', archivo_audio]
            elif sys.platform.startswith('linux'):
                # En Linux, intentar reproductores de audio sin interfaz
                reproductores = [
                    ['mpv', '--really-quiet', '--no-video', archivo_audio],
                    ['vlc', '--intf', 'dummy', '--play-and-exit', archivo_audio],
                    ['mplayer', '-really-quiet', archivo_audio],
                    ['aplay', archivo_audio] if archivo_audio.endswith('.wav') else None
                ]
                
                # Filtrar opciones None
                reproductores = [r for r in reproductores if r is not None]
                
                # Intentar cada reproductor
                for cmd in reproductores:
                    try:
                        result = subprocess.run(['which', cmd[0]], 
                                              capture_output=True, 
                                              timeout=1)
                        if result.returncode == 0:
                            break
                    except:
                        continue
                else:
                    # Fallback a reproductor por defecto
                    cmd = ['xdg-open', archivo_audio]
            else:
                # Windows - usar reproductor por defecto
                return os.startfile(archivo_audio)
            
            # Ejecutar comando
            process = subprocess.Popen(cmd, 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
            return process
            
        except Exception as e:
            print(f"Error al reproducir audio: {e}")
            return None
    
    def detectar_dispositivos_audio(self):
        """Detectar y listar dispositivos de audio disponibles"""
        try:
            p = pyaudio.PyAudio()
            print("🔍 Dispositivos de audio disponibles:")
            
            dispositivos = []
            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    dispositivos.append((i, info['name']))
                    print(f"   [{i}] {info['name']} - Canales: {info['maxInputChannels']}")
            
            p.terminate()
            return dispositivos
        except Exception as e:
            print(f"⚠️ Error al detectar dispositivos: {e}")
            return []
    
    def grabar_voz(self, input_device_index=None):
        """Grabar voz del usuario"""
        print("\n" + "="*60)
        print("🎙️ INICIANDO GRABACIÓN DE AUDIO")
        print("="*60)
        
        # Detectar dispositivos si es necesario
        if input_device_index is None:
            dispositivos = self.detectar_dispositivos_audio()
            if not dispositivos:
                print("❌ No se encontraron dispositivos de audio")
                return None
        
        try:
            p = pyaudio.PyAudio()
            
            # Configurar stream
            stream_config = {
                'format': self.FORMAT,
                'channels': self.CHANNELS,
                'rate': self.RATE,
                'input': True,
                'frames_per_buffer': self.CHUNK
            }
            
            if input_device_index is not None:
                stream_config['input_device_index'] = input_device_index
            
            stream = p.open(**stream_config)
            
            print(f"🔴 GRABANDO por {self.DURATION_SECONDS} segundos...")
            print("Texto sugerido: 'Hola, soy yo, y estoy haciendo esta grabación para crear")
            print("mi voz digital. Me encanta cómo la tecnología puede capturar cada detalle.'")
            print("IMPORTANTE: Habla CLARO y FUERTE durante todos los segundos.")
            print("-" * 60)
            
            frames = []
            
            # Capturar datos del micrófono
            for i in range(0, int(self.RATE / self.CHUNK * self.DURATION_SECONDS)):
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Mostrar progreso cada segundo aproximadamente
                    if i % (self.RATE // self.CHUNK) == 0:
                        segundos_restantes = self.DURATION_SECONDS - (i // (self.RATE // self.CHUNK))
                        print(f"   🎤 Grabando... {segundos_restantes}s restantes", end='\r')
                        
                except IOError as e:
                    print(f"Error de lectura: {e}")
                    continue
            
            print(f"\n✅ GRABACIÓN FINALIZADA")
            
            # Obtener sample_width ANTES de cerrar PyAudio
            sample_width = p.get_sample_size(self.FORMAT)
            
            # Cerrar stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Guardar archivo WAV
            with wave.open(self.FILENAME, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(sample_width)
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
            
            # Verificar archivo
            if os.path.exists(self.FILENAME):
                size = os.path.getsize(self.FILENAME)
                print(f"💾 Audio guardado: {self.FILENAME} ({size} bytes)")
                return self.FILENAME
            else:
                print("❌ Error: archivo no se guardó correctamente")
                return None
                
        except Exception as e:
            print(f"❌ Error durante la grabación: {e}")
            return None
    
    def esperar_voz_lista(self, voice_id, timeout_segundos=180):
        """Esperar a que la voz esté procesada en ElevenLabs"""
        headers = {"xi-api-key": self.API_KEY}
        waited = 0
        interval = 15
        
        print(f"⏳ Verificando que la voz {voice_id} esté procesada (timeout: {timeout_segundos}s)...")
        
        while waited < timeout_segundos:
            try:
                # Consultar la lista completa de voces del usuario
                response = requests.get(self.URL_GET_VOICES, headers=headers)
                
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
                        print(f"✅ Voz '{voice_name}' encontrada con {len(samples)} muestras procesadas")
                        
                        # Si tiene muestras, está lista para usar
                        if samples:
                            print(f"🎯 Voz lista para síntesis tras {waited}s")
                            return True
                        else:
                            print(f"⏳ Voz encontrada pero sin muestras aún... esperando")
                    else:
                        print(f"⏳ Voz {voice_id} aún no aparece en la lista... ({waited}s)")
                else:
                    print(f"❌ Error consultando voces: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error verificando voz: {e}")
            
            time.sleep(interval)
            waited += interval
        
        print(f"⚠️ Timeout alcanzado ({timeout_segundos}s). La voz podría no estar lista.")
        return False
    
    def clonar_voz(self, archivo_audio):
        """Clonar voz subiendo muestra a ElevenLabs"""
        print("\n" + "="*60)
        print("☁️ INICIANDO CLONACIÓN DE VOZ")
        print("="*60)
        
        if not os.path.exists(archivo_audio):
            print(f"❌ Archivo {archivo_audio} no encontrado")
            return None
        
        headers = {"xi-api-key": self.API_KEY}
        
        # Preparar datos para subir la voz
        data_upload = {
            'name': f'Temp_Voice_{int(time.time())}',
            'description': 'Voz temporal para experimento Nodo 2',
            'labels': '{"source": "nodo2_experiencia"}'
        }
        
        try:
            print(f"📤 Subiendo muestra: {os.path.basename(archivo_audio)}")
            
            with open(archivo_audio, 'rb') as audio_file:
                files = {'files': (os.path.basename(archivo_audio), audio_file, 'audio/wav')}
                
                response_upload = requests.post(
                    self.URL_ADD_VOICE,
                    headers=headers,
                    data=data_upload,
                    files=files
                )
                response_upload.raise_for_status()
            
            upload_json = response_upload.json()
            voice_id = upload_json.get('voice_id')
            
            if not voice_id:
                print(f"❌ No se obtuvo voice_id. Respuesta: {upload_json}")
                return None
            
            print(f"✅ Voz subida exitosamente. ID: {voice_id}")
            
            # Esperar a que la voz sea procesada
            print("⏳ ESPERANDO que ElevenLabs procese tu muestra de voz...")
            print("   Esto es CRÍTICO: sin esperar, ElevenLabs usará una voz genérica")
            
            voz_lista = self.esperar_voz_lista(voice_id, timeout_segundos=180)
            
            if not voz_lista:
                print("⚠️ WARNING: La voz podría no estar completamente procesada")
                print("   El resultado podría ser una voz genérica en lugar de la tuya")
            
            return voice_id
            
        except Exception as e:
            print(f"❌ Error durante clonación: {e}")
            return None
    
    def sintetizar_voz(self, voice_id):
        """Generar audio con la voz clonada"""
        print("\n" + "="*60)
        print("🎵 SINTETIZANDO CON VOZ CLONADA")
        print("="*60)
        
        if not voice_id:
            print("❌ ID de voz no válido")
            return None
        
        headers_synthesis = {
            "xi-api-key": self.API_KEY,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json"
        }
        
        data_synthesis = {
            "text": self.TEXTO_FINAL,
            "model_id": "eleven_multilingual_v2",  # Modelo multilingüe con mejor soporte para español
            "voice_settings": {
                "stability": 0.5,       # Estabilidad media para español
                "similarity_boost": 0.85, # Alta similitud a la muestra original
                "style": 0.1,           # Ligero estilo para naturalidad
                "use_speaker_boost": True
            }
        }
        
        try:
            print(f"🎯 Sintetizando con voz ID: {voice_id}")
            print(f"📝 Texto: '{self.TEXTO_FINAL[:60]}...'")
            
            response_synthesis = requests.post(
                f"{self.URL_TTS}{voice_id}",
                headers=headers_synthesis,
                json=data_synthesis
            )
            
            print(f"📡 Respuesta HTTP: {response_synthesis.status_code}")
            
            if response_synthesis.status_code != 200:
                print(f"❌ ERROR HTTP {response_synthesis.status_code}")
                print(f"   Respuesta: {response_synthesis.text}")
                return None
            
            response_synthesis.raise_for_status()
            
            # Análisis de la respuesta
            content_size = len(response_synthesis.content)
            print(f"📦 Audio recibido: {content_size} bytes")
            
            # Verificaciones de calidad
            if content_size < 2000:
                print("❌ PROBLEMA GRAVE: Archivo demasiado pequeño!")
                print("   Esto indica que ElevenLabs NO usó tu voz clonada")
            elif content_size < 5000:
                print("⚠️ Archivo pequeño - podría ser voz genérica")
            else:
                print("✅ Tamaño correcto - probablemente es tu voz clonada")
            
            # Guardar el archivo
            with open(self.ARCHIVO_FINAL, 'wb') as f:
                f.write(response_synthesis.content)
            
            final_size = os.path.getsize(self.ARCHIVO_FINAL)
            print(f"✅ MP3 guardado: {self.ARCHIVO_FINAL} ({final_size} bytes)")
            
            return self.ARCHIVO_FINAL
            
        except Exception as e:
            print(f"❌ Error en síntesis: {e}")
            return None
    
    def reproducir_resultado(self, archivo_mp3):
        """Reproducir el resultado final (solo audio, sin ventana)"""
        if not archivo_mp3 or not os.path.exists(archivo_mp3):
            print(f"❌ Archivo {archivo_mp3} no encontrado")
            return False
        
        try:
            print(f"🔊 Reproduciendo resultado: {archivo_mp3}")
            # Usar reproductor de solo audio para no interferir con la interfaz
            process = self.reproducir_solo_audio(archivo_mp3)
            
            if process:
                # Dar tiempo para que inicie la reproducción
                time.sleep(3)
                print("🎵 Audio reproduciéndose sin ventana...")
                return True
            else:
                print("⚠️ No se pudo iniciar reproductor de audio")
                return False
            
        except Exception as e:
            print(f"❌ Error al reproducir: {e}")
            return False
    
    def limpiar_voz(self, voice_id):
        """Eliminar voz temporal de ElevenLabs"""
        if not voice_id:
            print("⚠️ No hay voz para eliminar")
            return True
        
        print(f"🧹 Limpiando voz temporal: {voice_id}")
        
        headers = {"xi-api-key": self.API_KEY}
        
        try:
            response = requests.delete(f"{self.URL_DELETE_VOICE}{voice_id}", headers=headers)
            response.raise_for_status()
            print("✅ Voz temporal eliminada del servidor")
            return True
        except Exception as e:
            print(f"⚠️ Error eliminando voz {voice_id}: {e}")
            print("   Elimínala manualmente desde console.elevenlabs.io")
            return False
    
    def ejecutar_experiencia_completa(self):
        """Ejecutar toda la experiencia de clonación de voz"""
        print("\n" + "="*70)
        print("       🎤 EXPERIENCIA DE CLONACIÓN DE VOZ - NODO 2")
        print("="*70)
        print("Proceso:")
        print("1. 🎤 Grabar tu voz (13 segundos)")
        print("2. ☁️  Clonar tu voz en ElevenLabs")
        print("3. 🎵 Sintetizar frase final con tu voz clonada")
        print("4. 🔊 Reproducir resultado automáticamente")
        print("5. 🧹 Limpiar recursos temporales")
        print("="*70)
        
        try:
            # PASO 1: Grabar audio
            print("\n🎤 PASO 1: Grabación de audio")
            archivo_audio = self.grabar_voz()
            
            if not archivo_audio:
                print("❌ Error en la grabación. Abortando.")
                return False
            
            # PASO 2: Clonar voz
            print("\n☁️ PASO 2: Clonación de voz")
            voice_id = self.clonar_voz(archivo_audio)
            
            if not voice_id:
                print("❌ Error en la clonación. Abortando.")
                return False
            
            # PASO 3: Sintetizar
            print("\n🎵 PASO 3: Síntesis de voz")
            archivo_mp3 = self.sintetizar_voz(voice_id)
            
            if not archivo_mp3:
                print("❌ Error en la síntesis.")
                self.limpiar_voz(voice_id)
                return False
            
            # PASO 4: Reproducir resultado
            print("\n🔊 PASO 4: Reproducción del resultado")
            self.reproducir_resultado(archivo_mp3)
            
            # PASO 5: Limpiar
            print("\n🧹 PASO 5: Limpieza")
            self.limpiar_voz(voice_id)
            
            # Resultado final
            print("\n" + "="*70)
            if archivo_mp3 and os.path.exists(archivo_mp3):
                size_kb = os.path.getsize(archivo_mp3) / 1024
                print(f"🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
                print(f"📁 Archivos generados:")
                print(f"   • Audio original grabado: {archivo_audio}")
                print(f"   • Tu voz clonada: {archivo_mp3} ({size_kb:.1f} KB)")
                print(f"\n🎯 QUE DEBERÍAS ESCUCHAR:")
                print(f"   '{self.TEXTO_FINAL[:60]}...'")
                print(f"   Con tu PROPIA VOZ")
                
                if size_kb < 10:
                    print(f"\n⚠️  DIAGNÓSTICO: Archivo muy pequeño ({size_kb:.1f} KB)")
                    print("   PROBABLE CAUSA: ElevenLabs NO usó tu voz clonada")
                elif size_kb > 30:
                    print(f"\n✅ Tamaño correcto ({size_kb:.1f} KB) - probablemente tu voz clonada")
            else:
                print("❌ Error: No se pudo completar el proceso")
            
            print("="*70)
            return True
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Proceso interrumpido por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            return False

def main():
    """Función principal para ejecutar directamente este módulo"""
    clonador = LogicaClonacion()
    clonador.ejecutar_experiencia_completa()

if __name__ == "__main__":
    main()
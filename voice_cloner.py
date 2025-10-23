#!/usr/bin/env python3
# =====================================================
# MÓDULO DE CLONACIÓN DE VOZ - ElevenLabs + PyAudio
# =====================================================
# Módulo modular para la experiencia de clonación de voz
# Separado de la interfaz para mejor organización del código

import pyaudio
import wave
import time
import os
import sys
import subprocess
import requests

class VoiceCloner:
    """Clase para manejar todo el proceso de clonación de voz"""
    
    def __init__(self):
        # Configuración de ElevenLabs
        self.API_KEY = "8007664948e8dd45023e33e533ca8c3782511d7d62913ee436b83bc36ea16746"
        self.TEXTO_FINAL = "Gracias por regalarnos tu voz, ahora tengo el poder de hablar como tú, usarla para los fines que quiera, porque ahora es propiedad de nodo 2."
        
        # Archivos
        self.ARCHIVO_FINAL = "frase_final_clonada.mp3"
        self.VIDEO_FILE = 'instrucciones.mp4'
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
            
    def reproducir_instrucciones(self):
        """Reproducir video de instrucciones"""
        print(f"🎬 PASO 1: Reproduciendo {self.VIDEO_FILE}")
        
        if not os.path.exists(self.VIDEO_FILE):
            print(f"⚠️ Archivo {self.VIDEO_FILE} no encontrado")
            return False
            
        try:
            self.abrir_archivo(self.VIDEO_FILE)
            print(f"✅ Video iniciado: {self.VIDEO_FILE}")
            
            # Countdown automático de 12 segundos
            print("\n⏱️ Esperando 12 segundos antes de la grabación...")
            for i in range(12, 0, -1):
                print(f"   Grabación comenzará en: {i} segundos", end='\r')
                time.sleep(1)
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al reproducir video: {e}")
            return False
            
    def detectar_dispositivos_audio(self):
        """Detectar y listar dispositivos de audio disponibles"""
        try:
            p = pyaudio.PyAudio()
            print("🔍 Dispositivos de audio disponibles:")
            
            devices = []
            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:  # Solo dispositivos de entrada
                    devices.append((i, info['name']))
                    print(f"   [{i}] {info['name']} - Canales: {info['maxInputChannels']}")
                    
            p.terminate()
            return devices
            
        except Exception as e:
            print(f"⚠️ Error al detectar dispositivos: {e}")
            return []
            
    def grabar_voz(self):
        """Grabar voz del usuario"""
        print(f"\n🎙️ PASO 2: Grabación de voz")
        
        # Detectar dispositivos
        dispositivos = self.detectar_dispositivos_audio()
        if not dispositivos:
            print("❌ No se encontraron dispositivos de audio")
            return None
            
        try:
            p = pyaudio.PyAudio()
            
            # Configurar stream
            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            print(f"🔴 GRABANDO... Habla durante {self.DURATION_SECONDS} segundos")
            
            frames = []
            
            # Grabar con countdown visual
            for i in range(0, int(self.RATE / self.CHUNK * self.DURATION_SECONDS)):
                data = stream.read(self.CHUNK)
                frames.append(data)
                
                # Mostrar progreso cada segundo aproximadamente
                if i % (self.RATE // self.CHUNK) == 0:
                    segundos_restantes = self.DURATION_SECONDS - (i // (self.RATE // self.CHUNK))
                    print(f"   🎤 Grabando... {segundos_restantes}s restantes", end='\r')
                    
            print(f"\n✅ Grabación completada: {self.DURATION_SECONDS} segundos")
            
            # Detener y cerrar stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Guardar archivo WAV
            with wave.open(self.FILENAME, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                
            # Verificar archivo
            if os.path.exists(self.FILENAME):
                size = os.path.getsize(self.FILENAME)
                print(f"📁 Archivo guardado: {self.FILENAME} ({size} bytes)")
                return self.FILENAME
            else:
                print("❌ Error: archivo no se guardó correctamente")
                return None
                
        except Exception as e:
            print(f"❌ Error durante la grabación: {e}")
            return None
            
    def clonar_voz(self, archivo_voz):
        """Subir voz a ElevenLabs y crear clon"""
        print(f"\n☁️ PASO 3: Clonando voz en ElevenLabs")
        
        if not os.path.exists(archivo_voz):
            print(f"❌ Archivo {archivo_voz} no encontrado")
            return None
            
        try:
            headers = {"xi-api-key": self.API_KEY}
            
            # Preparar datos para subir
            data = {
                'name': f'VozTemporal_{int(time.time())}',
                'labels': '{"accent": "spanish", "description": "Voz temporal para experimento"}'
            }
            
            with open(archivo_voz, 'rb') as f:
                files = {'files': (archivo_voz, f, 'audio/wav')}
                
                print("📤 Subiendo voz para clonación...")
                response = requests.post(self.URL_ADD_VOICE, headers=headers, data=data, files=files)
                
            print(f"📊 Respuesta del servidor: {response.status_code}")
            
            if response.status_code == 200:
                response_json = response.json()
                voice_id = response_json['voice_id']
                print(f"✅ Voz clonada exitosamente - ID: {voice_id}")
                
                # Esperar a que la voz esté lista
                return self.esperar_voz_lista(voice_id)
                
            else:
                print(f"❌ Error al clonar voz: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error durante clonación: {e}")
            return None
            
    def esperar_voz_lista(self, voice_id):
        """Esperar a que la voz esté lista para usar con timeout extendido"""
        print("⏳ Esperando a que la voz esté lista...")
        
        headers = {"xi-api-key": self.API_KEY}
        max_intentos = 60  # Aumentado de 30 a 60 (2 minutos)
        tiempo_espera = 3  # Aumentado de 2 a 3 segundos
        
        for intento in range(max_intentos):
            try:
                print(f"   🔍 Verificando estado... ({intento + 1}/{max_intentos})")
                response = requests.get(f"{self.URL_GET_VOICES}/{voice_id}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    voice_data = response.json()
                    status = voice_data.get('status', 'unknown')
                    
                    print(f"   📊 Estado actual: {status}")
                    
                    if status == 'ready':
                        print("✅ Voz lista para sintetizar")
                        return voice_id
                    elif status == 'failed':
                        print("❌ La clonación de voz falló en el servidor")
                        return None
                    elif status in ['processing', 'training']:
                        print(f"   🔄 Procesando... quedan {max_intentos - intento - 1} intentos")
                    
                    time.sleep(tiempo_espera)
                    
                else:
                    print(f"⚠️ Error al verificar estado: {response.status_code}")
                    if intento < 5:  # Solo reintentar los primeros 5 errores
                        time.sleep(tiempo_espera)
                    else:
                        print("❌ Demasiados errores de conexión")
                        return None
                    
            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout en intento {intento + 1}")
                time.sleep(tiempo_espera)
            except Exception as e:
                print(f"⚠️ Error en verificación: {e}")
                time.sleep(tiempo_espera)
                
        print("❌ Timeout: la voz no estuvo lista después de 3 minutos")
        print("   Esto puede ocurrir si:")
        print("   - El servidor está sobrecargado")
        print("   - La grabación tiene problemas de calidad")
        print("   - Hay problemas de conectividad")
        return None
        
    def sintetizar_voz(self, voice_id):
        """Generar audio con la voz clonada"""
        print(f"\n🤖 PASO 4: Sintetizando frase con voz clonada")
        
        if not voice_id:
            print("❌ ID de voz no válido")
            return None
            
        try:
            headers = {
                "xi-api-key": self.API_KEY,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": self.TEXTO_FINAL,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            print("🎵 Generando audio con voz clonada...")
            response = requests.post(f"{self.URL_TTS}{voice_id}", headers=headers, json=data)
            
            if response.status_code == 200:
                with open(self.ARCHIVO_FINAL, 'wb') as f:
                    f.write(response.content)
                    
                print(f"✅ Audio generado: {self.ARCHIVO_FINAL}")
                return self.ARCHIVO_FINAL
                
            else:
                print(f"❌ Error al sintetizar: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error durante síntesis: {e}")
            return None
            
    def reproducir_resultado(self, archivo_mp3):
        """Reproducir el resultado final"""
        print(f"\n🔊 PASO 5: Reproduciendo resultado")
        
        if not archivo_mp3 or not os.path.exists(archivo_mp3):
            print(f"❌ Archivo {archivo_mp3} no encontrado")
            return False
            
        try:
            print(f"🎵 Reproduciendo: {archivo_mp3}")
            self.abrir_archivo(archivo_mp3)
            
            # Dar tiempo para que inicie la reproducción
            time.sleep(3)
            print("✅ Reproducción iniciada")
            return True
            
        except Exception as e:
            print(f"❌ Error al reproducir: {e}")
            return False
            
    def limpiar_voz(self, voice_id):
        """Eliminar voz temporal de ElevenLabs"""
        print(f"\n🗑️ PASO 6: Limpiando datos temporales")
        
        if not voice_id:
            print("⚠️ No hay voz para eliminar")
            return True
            
        try:
            headers = {"xi-api-key": self.API_KEY}
            response = requests.delete(f"{self.URL_DELETE_VOICE}{voice_id}", headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Voz eliminada del servidor: {voice_id}")
                return True
            else:
                print(f"⚠️ Error al eliminar voz: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ Error durante limpieza: {e}")
            return False
            
    def ejecutar_experiencia_completa(self):
        """Ejecutar toda la experiencia de principio a fin"""
        print("🎤 INICIANDO EXPERIENCIA DE CLONACIÓN DE VOZ")
        print("=" * 50)
        
        try:
            # Paso 1: Reproducir instrucciones
            if not self.reproducir_instrucciones():
                return False
                
            # Paso 2: Grabar voz
            archivo_voz = self.grabar_voz()
            if not archivo_voz:
                return False
                
            # Paso 3: Clonar voz
            voice_id = self.clonar_voz(archivo_voz)
            if not voice_id:
                return False
                
            # Paso 4: Sintetizar
            archivo_final = self.sintetizar_voz(voice_id)
            if not archivo_final:
                return False
                
            # Paso 5: Reproducir resultado
            self.reproducir_resultado(archivo_final)
            
            # Paso 6: Limpiar
            self.limpiar_voz(voice_id)
            
            print("\n🎉 EXPERIENCIA COMPLETADA EXITOSAMENTE")
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR EN LA EXPERIENCIA: {e}")
            return False

def main():
    """Función principal para ejecutar directamente este módulo"""
    cloner = VoiceCloner()
    cloner.ejecutar_experiencia_completa()

if __name__ == "__main__":
    main()
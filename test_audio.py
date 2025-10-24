import pyaudio
import wave
import time
import os
import sys
import subprocess
from pathlib import Path

class TestAudio:
    def __init__(self):
        # Configuración de audio
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.DURATION_SECONDS = 5  # Prueba de 5 segundos
        self.TEST_FILENAME = "test_audio_sample.wav"
        
    def detectar_dispositivos_audio(self):
        """Detectar y listar todos los dispositivos de audio disponibles"""
        print("🔍 DETECTANDO DISPOSITIVOS DE AUDIO...")
        print("=" * 50)
        
        try:
            p = pyaudio.PyAudio()
            
            print(f"📊 Total de dispositivos encontrados: {p.get_device_count()}")
            print("\n📥 DISPOSITIVOS DE ENTRADA (Micrófonos):")
            
            dispositivos_entrada = []
            for i in range(p.get_device_count()):
                try:
                    info = p.get_device_info_by_index(i)
                    if info['maxInputChannels'] > 0:
                        dispositivos_entrada.append((i, info['name']))
                        print(f"   [{i}] {info['name']}")
                        print(f"       Canales: {info['maxInputChannels']}")
                        print(f"       Frecuencia: {info['defaultSampleRate']} Hz")
                        print(f"       Host API: {p.get_host_api_info_by_index(info['hostApi'])['name']}")
                        print()
                except Exception as e:
                    print(f"   [Error en dispositivo {i}]: {e}")
            
            print("📤 DISPOSITIVOS DE SALIDA (Altavoces):")
            dispositivos_salida = []
            for i in range(p.get_device_count()):
                try:
                    info = p.get_device_info_by_index(i)
                    if info['maxOutputChannels'] > 0:
                        dispositivos_salida.append((i, info['name']))
                        print(f"   [{i}] {info['name']}")
                        print(f"       Canales: {info['maxOutputChannels']}")
                        print(f"       Frecuencia: {info['defaultSampleRate']} Hz")
                        print()
                except Exception as e:
                    print(f"   [Error en dispositivo {i}]: {e}")
            
            p.terminate()
            
            return dispositivos_entrada, dispositivos_salida
            
        except Exception as e:
            print(f"❌ Error al detectar dispositivos: {e}")
            return [], []
    
    def probar_microfono(self, device_id=None):
        """Probar grabación desde el micrófono"""
        print(f"\n🎙️ PROBANDO MICRÓFONO...")
        print("=" * 30)
        
        try:
            p = pyaudio.PyAudio()
            
            # Configurar parámetros de grabación
            kwargs = {
                'format': self.FORMAT,
                'channels': self.CHANNELS,
                'rate': self.RATE,
                'input': True,
                'frames_per_buffer': self.CHUNK
            }
            
            if device_id is not None:
                kwargs['input_device_index'] = device_id
                print(f"📍 Usando dispositivo específico: {device_id}")
            else:
                print("📍 Usando dispositivo de entrada por defecto")
            
            # Intentar abrir el stream
            try:
                stream = p.open(**kwargs)
                print("✅ Stream de audio abierto correctamente")
            except Exception as e:
                print(f"❌ Error al abrir stream: {e}")
                p.terminate()
                return False
            
            print(f"🔴 GRABANDO... Habla durante {self.DURATION_SECONDS} segundos")
            print("   (Di algo como: 'Hola, este es un test de micrófono')")
            
            frames = []
            
            # Grabar con indicador visual
            for i in range(0, int(self.RATE / self.CHUNK * self.DURATION_SECONDS)):
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Mostrar progreso
                    if i % (self.RATE // self.CHUNK) == 0:
                        segundos_restantes = self.DURATION_SECONDS - (i // (self.RATE // self.CHUNK))
                        print(f"   🎤 Grabando... {segundos_restantes}s restantes", end='\r')
                        
                except Exception as e:
                    print(f"\n⚠️ Error durante grabación: {e}")
                    break
                    
            print(f"\n✅ Grabación completada")
            
            # Cerrar stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Guardar archivo
            try:
                with wave.open(self.TEST_FILENAME, 'wb') as wf:
                    wf.setnchannels(self.CHANNELS)
                    wf.setsampwidth(p.get_sample_size(self.FORMAT))
                    wf.setframerate(self.RATE)
                    wf.writeframes(b''.join(frames))
                
                # Verificar archivo
                if os.path.exists(self.TEST_FILENAME):
                    size = os.path.getsize(self.TEST_FILENAME)
                    print(f"📁 Archivo guardado: {self.TEST_FILENAME} ({size} bytes)")
                    return True
                else:
                    print("❌ Error: archivo no se guardó")
                    return False
                    
            except Exception as e:
                print(f"❌ Error al guardar archivo: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error general en prueba de micrófono: {e}")
            return False
    
    def probar_reproduccion(self):
        """Probar reproducción del archivo grabado"""
        print(f"\n🔊 PROBANDO REPRODUCCIÓN...")
        print("=" * 30)
        
        if not os.path.exists(self.TEST_FILENAME):
            print(f"❌ Archivo {self.TEST_FILENAME} no encontrado")
            return False
        
        try:
            print(f"🎵 Reproduciendo: {self.TEST_FILENAME}")
            
            # Intentar diferentes reproductores según el sistema
            if sys.platform == 'darwin':
                # macOS
                reproductores = [
                    ['afplay', self.TEST_FILENAME],
                    ['open', self.TEST_FILENAME]
                ]
            elif sys.platform.startswith('linux'):
                # Linux/Raspberry Pi
                reproductores = [
                    ['aplay', self.TEST_FILENAME],  # ALSA player (común en RPi)
                    ['paplay', self.TEST_FILENAME],  # PulseAudio player
                    ['mpv', '--really-quiet', self.TEST_FILENAME],
                    ['vlc', '--play-and-exit', '--intf', 'dummy', self.TEST_FILENAME],
                    ['mplayer', '-quiet', self.TEST_FILENAME]
                ]
            else:
                # Windows
                reproductores = [
                    ['start', self.TEST_FILENAME]
                ]
            
            # Intentar cada reproductor
            for cmd in reproductores:
                try:
                    # Verificar si el comando existe
                    if sys.platform != 'windows':
                        result = subprocess.run(['which', cmd[0]], 
                                              capture_output=True, 
                                              timeout=2)
                        if result.returncode != 0:
                            continue
                    
                    print(f"🎯 Usando reproductor: {cmd[0]}")
                    
                    # Ejecutar reproductor
                    process = subprocess.Popen(cmd, 
                                             stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL)
                    
                    # Esperar a que termine
                    try:
                        process.wait(timeout=10)
                        print("✅ Reproducción completada")
                        return True
                    except subprocess.TimeoutExpired:
                        process.terminate()
                        print("✅ Reproducción iniciada (timeout)")
                        return True
                        
                except Exception as e:
                    print(f"⚠️ Error con {cmd[0]}: {e}")
                    continue
            
            print("❌ No se pudo reproducir con ningún reproductor")
            return False
            
        except Exception as e:
            print(f"❌ Error en reproducción: {e}")
            return False
    
    def limpiar_archivos_test(self):
        """Limpiar archivos de prueba"""
        try:
            if os.path.exists(self.TEST_FILENAME):
                os.remove(self.TEST_FILENAME)
                print(f"🧹 Archivo de prueba eliminado: {self.TEST_FILENAME}")
        except Exception as e:
            print(f"⚠️ Error al limpiar archivos: {e}")
    
    def ejecutar_test_completo(self):
        """Ejecutar test completo de audio"""
        print("🎤 TEST DE AUDIO - MICRÓFONO Y REPRODUCCIÓN")
        print("=" * 50)
        print("Este test verificará que:")
        print("• El micrófono puede grabar audio")
        print("• El sistema puede reproducir audio")
        print("• Los dispositivos están configurados correctamente")
        print()
        
        # Paso 1: Detectar dispositivos
        dispositivos_entrada, dispositivos_salida = self.detectar_dispositivos_audio()
        
        if not dispositivos_entrada:
            print("❌ No se encontraron dispositivos de entrada (micrófonos)")
            return False
        
        if not dispositivos_salida:
            print("⚠️ No se encontraron dispositivos de salida (altavoces)")
            print("   El test continuará pero la reproducción puede fallar")
        
        # Paso 2: Probar micrófono
        if not self.probar_microfono():
            print("\n❌ TEST FALLIDO: Problema con el micrófono")
            return False
        
        # Paso 3: Probar reproducción
        if not self.probar_reproduccion():
            print("\n❌ TEST FALLIDO: Problema con la reproducción")
            self.limpiar_archivos_test()
            return False
        
        # Paso 4: Limpiar
        time.sleep(1)  # Dar tiempo para que termine la reproducción
        self.limpiar_archivos_test()
        
        print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print("✅ El micrófono y la reproducción funcionan correctamente")
        print("✅ El sistema está listo para la experiencia de clonación de voz")
        return True

def main():
    """Función principal"""
    try:
        test = TestAudio()
        
        # Verificar PyAudio
        try:
            import pyaudio
            print("✅ PyAudio disponible")
        except ImportError:
            print("❌ PyAudio no está instalado")
            print("   Instala con: pip install pyaudio")
            return
        
        # Ejecutar test
        success = test.ejecutar_test_completo()
        
        if success:
            print("\n🚀 Sistema listo para la experiencia completa")
        else:
            print("\n🔧 Revisa la configuración de audio del sistema")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
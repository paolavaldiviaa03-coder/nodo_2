# 🎤 Experiencia de Clonación de Voz - Nodo 2

Una experiencia interactiva que permite a los usuarios clonar su voz usando inteligencia artificial.

## 🎯 ¿Qué hace este programa?

1. **📹 Video de instrucciones**: Reproduce un video explicativo
2. **🎙️ Grabación de voz**: Captura 13 segundos de audio del usuario
3. **🤖 Clonación IA**: Usa ElevenLabs para clonar la voz
4. **🔊 Reproducción**: Reproduce el resultado con la voz clonada
5. **🗑️ Limpieza**: Elimina la voz de los servidores por privacidad

## 🚀 Inicio Rápido

### Opción 1: Interfaz Gráfica (Recomendado)
```bash
python main.py
```

### Opción 2: Solo Consola
```bash
python voice_cloner.py
```

### Opción 3: Código Original
```bash
python "import pyaudio.py"
```

## 📋 Requisitos del Sistema

### Software Necesario
- **Python 3.7+**
- **Micrófono funcionando**
- **Conexión a internet**
- **Reproductor de video** (VLC recomendado)

### Para Ubuntu/Debian/Raspberry Pi:
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3-pip python3-tk vlc ffmpeg

# Instalar dependencias de audio
sudo apt install -y portaudio19-dev python3-pyaudio alsa-utils

# Si tienes problemas con PyAudio:
sudo apt install -y libasound2-dev
```

### Para macOS:
```bash
# Con Homebrew
brew install portaudio ffmpeg vlc

# Instalar dependencias Python
pip install -r requirements.txt
```

### Para Windows:
```bash
# Descargar VLC desde: https://www.videolan.org/vlc/
# Instalar dependencias Python
pip install -r requirements.txt
```

## 🔧 Instalación

### 1. Clonar/Descargar el proyecto
```bash
git clone <este-repositorio>
cd proyecto_pao
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

### 3. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 4. Verificar archivos necesarios
Asegúrate de tener:
- ✅ `instrucciones.mp4` - Video explicativo
- ✅ `main.py` - Lanzador principal
- ✅ `interfaz_experiencia.py` - Interfaz gráfica
- ✅ `voice_cloner.py` - Lógica de clonación
- ✅ `requirements.txt` - Dependencias

## 🎮 Uso

### Para la Experiencia Completa:
1. Ejecuta `python main.py`
2. Haz clic en "🚀 INICIAR EXPERIENCIA"
3. Sigue las instrucciones en pantalla
4. ¡Escucha tu voz clonada!

### Estructura de la Experiencia:
```
🎬 Paso 1: Video de instrucciones (automático)
     ↓ 
⏱️  Countdown de 12 segundos
     ↓
🎙️  Paso 2: Grabación de voz (13 segundos)
     ↓
☁️  Paso 3: Subida a ElevenLabs
     ↓
🤖 Paso 4: Clonación de voz
     ↓
🔊 Paso 5: Reproducción del resultado
     ↓
🗑️  Paso 6: Limpieza (eliminación de datos)
```

## 🛠️ Solución de Problemas

### Error: "could not find a valid device"
```bash
# Linux: Verificar dispositivos de audio
aplay -l
arecord -l

# Instalar ALSA utilities
sudo apt install -y alsa-utils

# Configurar micrófono por defecto
alsamixer
```

### Error: "cant configure decoder"
```bash
# Instalar codecs adicionales
sudo apt install -y ubuntu-restricted-extras ffmpeg

# Para Raspberry Pi:
sudo apt install -y vlc-plugin-base
```

### Error: "PyAudio no instalado"
```bash
# Ubuntu/Debian:
sudo apt install -y python3-pyaudio

# Si no funciona:
sudo apt install -y portaudio19-dev
pip install pyaudio

# macOS:
brew install portaudio
pip install pyaudio
```

### Error: "Tkinter no disponible"
```bash
# Ubuntu/Debian:
sudo apt install -y python3-tk

# CentOS/RHEL:
sudo yum install -y tkinter
```

### Audio se satura o distorsiona
- Reduce el volumen del micrófono
- Aleja el micrófono de la boca
- Usa audífonos para evitar retroalimentación

## 🔒 Privacidad y Seguridad

- ✅ **Tu voz se elimina automáticamente** de los servidores de ElevenLabs
- ✅ **Solo se usa temporalmente** para la clonación
- ✅ **No se almacena permanentemente** en nuestros sistemas
- ✅ **El proceso es transparente** y puedes ver cada paso

## 📁 Estructura del Proyecto

```
proyecto_pao/
├── main.py                    # 🚀 Lanzador principal
├── interfaz_experiencia.py    # 🖥️ Interfaz gráfica
├── voice_cloner.py           # 🤖 Lógica de clonación
├── import pyaudio.py         # 📜 Código original
├── instrucciones.mp4         # 📹 Video explicativo
├── requirements.txt          # 📦 Dependencias
├── README.md                # 📖 Este archivo
├── LINUX_SETUP.md          # 🐧 Guía específica para Linux
└── env/                     # 🌐 Entorno virtual (después de instalación)
```

## 🎨 Características de la Interfaz

- **🖥️ Interfaz moderna** con tema oscuro
- **📊 Barra de progreso** en tiempo real
- **📝 Log de actividad** detallado
- **🔄 Manejo de errores** robusto
- **⚡ Ejecución en hilos** (no bloquea la interfaz)
- **💡 Confirmaciones** antes de acciones importantes

## 🌍 Compatibilidad

| Sistema | Estado | Notas |
|---------|--------|-------|
| 🐧 Linux | ✅ Completamente compatible | Incluye Raspberry Pi |
| 🍎 macOS | ✅ Completamente compatible | Requiere Homebrew para dependencias |
| 🪟 Windows | ✅ Completamente compatible | Usar PowerShell o CMD |

## 📞 Soporte

Si encuentras problemas:

1. **Revisa este README** completamente
2. **Verifica dependencias** con `python main.py`
3. **Consulta LINUX_SETUP.md** para problemas específicos de Linux
4. **Ejecuta el diagnóstico**: `python check_deps.py`

## 🏷️ Versión

- **Versión**: 2.0
- **Fecha**: Octubre 2025
- **Autor**: Nodo 2
- **Licencia**: Uso experimental/educativo

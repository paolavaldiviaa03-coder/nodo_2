# Configuración para Linux/Raspberry Pi

## Instalación de Dependencias Multimedia

### Para Ubuntu/Debian (incluye Raspberry Pi OS):

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas multimedia
sudo apt install -y mpg123 vlc ffmpeg

# Instalar dependencias de audio
sudo apt install -y alsa-utils pulseaudio

# Verificar audio
aplay -l  # Listar dispositivos de audio
alsamixer  # Ajustar volúmenes
```

### Para CentOS/RHEL/Fedora:

```bash
# Instalar herramientas multimedia
sudo yum install -y mpg123 vlc ffmpeg
# o para Fedora:
sudo dnf install -y mpg123 vlc ffmpeg
```

## Configuración de Audio en Raspberry Pi

```bash
# Configurar salida de audio (HDMI/Jack)
sudo raspi-config
# Ir a: Advanced Options > Audio > Force 3.5mm jack

# O por línea de comandos:
sudo amixer cset numid=3 1  # Para jack 3.5mm
sudo amixer cset numid=3 2  # Para HDMI
```

## Configuración de Video

```bash
# Asegurar que X11 está corriendo para visualización
export DISPLAY=:0.0

# Para sistemas sin interfaz gráfica, instalar:
sudo apt install -y xorg openbox
```

## Solución de Problemas

### Si no reproduce video:
```bash
# Verificar reproductores disponibles
which vlc
which mpv
which xdg-open

# Instalar reproductor alternativo
sudo apt install -y mpv
```

### Si no reproduce audio:
```bash
# Verificar dispositivos
aplay -l
arecord -l

# Probar reproducción
mpg123 --list-devices
aplay /usr/share/sounds/alsa/Front_Left.wav
```

### Permisos de audio:
```bash
# Agregar usuario al grupo audio
sudo usermod -a -G audio $USER
# Reiniciar sesión después de este comando
```

## Funcionamiento del Script

El script detecta automáticamente si está corriendo en Linux y activa el modo de reproducción simultánea:

1. **Video warning**: Se reproduce `warning.mp4` usando `xdg-open`
2. **Audio clonado**: Se reproduce usando `mpg123` (preferido) o `aplay` como fallback
3. **Sincronización**: El video inicia primero, luego el audio con pequeña pausa

### Orden de reproducción en Linux:
1. Inicia `warning.mp4` en background
2. Pausa 1 segundo
3. Reproduce `frase_final_clonada.mp3`
4. Espera a que termine el audio

### Fallbacks disponibles:
- Si `mpg123` no está: usa `aplay`
- Si `aplay` no está: usa `xdg-open`
- Si `warning.mp4` no existe: solo reproduce audio
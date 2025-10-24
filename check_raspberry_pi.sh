#!/bin/bash
# =====================================================
# TEST DE SISTEMA RASPBERRY PI OS
# =====================================================
# Script para verificar dependencias y configuración
# específica para Raspberry Pi OS

echo "🍓 VERIFICACIÓN PARA RASPBERRY PI OS"
echo "===================================="

# Verificar sistema operativo
echo "📊 INFORMACIÓN DEL SISTEMA:"
echo "Sistema: $(uname -s)"
echo "Arquitectura: $(uname -m)"
if [ -f /etc/os-release ]; then
    echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"')"
fi
echo ""

# Verificar Python y entorno virtual
echo "🐍 VERIFICANDO PYTHON:"
if command -v python3 &> /dev/null; then
    echo "✅ Python3 disponible: $(python3 --version)"
else
    echo "❌ Python3 no encontrado"
    exit 1
fi

if [ -d "env" ]; then
    echo "✅ Entorno virtual encontrado"
    source env/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "❌ Entorno virtual no encontrado"
    echo "   Ejecuta: python3 -m venv env"
    exit 1
fi
echo ""

# Verificar dependencias de audio
echo "🔊 VERIFICANDO DEPENDENCIAS DE AUDIO:"

# ALSA (Advanced Linux Sound Architecture)
if command -v aplay &> /dev/null; then
    echo "✅ ALSA disponible"
    echo "   Dispositivos ALSA:"
    aplay -l 2>/dev/null | grep -E "^card" | head -3
else
    echo "⚠️ ALSA no encontrado"
    echo "   Instala con: sudo apt-get install alsa-utils"
fi

# PulseAudio
if command -v pactl &> /dev/null; then
    echo "✅ PulseAudio disponible"
    if pactl info &> /dev/null; then
        echo "✅ PulseAudio corriendo"
    else
        echo "⚠️ PulseAudio no está corriendo"
    fi
else
    echo "⚠️ PulseAudio no encontrado"
    echo "   Instala con: sudo apt-get install pulseaudio"
fi
echo ""

# Verificar reproductores de video
echo "🎬 VERIFICANDO REPRODUCTORES DE VIDEO:"

# OMXPlayer (específico de Raspberry Pi)
if command -v omxplayer &> /dev/null; then
    echo "✅ OMXPlayer disponible (Raspberry Pi nativo)"
else
    echo "⚠️ OMXPlayer no encontrado"
    echo "   Instala con: sudo apt-get install omxplayer"
fi

# VLC
if command -v vlc &> /dev/null; then
    echo "✅ VLC disponible"
else
    echo "⚠️ VLC no encontrado"
    echo "   Instala con: sudo apt-get install vlc"
fi

# MPV
if command -v mpv &> /dev/null; then
    echo "✅ MPV disponible"
else
    echo "⚠️ MPV no encontrado"
    echo "   Instala con: sudo apt-get install mpv"
fi

# FFmpeg
if command -v ffplay &> /dev/null; then
    echo "✅ FFplay disponible"
else
    echo "⚠️ FFplay no encontrado"
    echo "   Instala con: sudo apt-get install ffmpeg"
fi
echo ""

# Verificar PyAudio
echo "🎙️ VERIFICANDO PYAUDIO:"
python3 -c "import pyaudio; print('✅ PyAudio disponible')" 2>/dev/null || {
    echo "❌ PyAudio no disponible"
    echo "   Para Raspberry Pi OS, instala dependencias:"
    echo "   sudo apt-get install python3-dev libasound2-dev"
    echo "   pip install pyaudio"
}
echo ""

# Verificar otras dependencias Python
echo "📦 VERIFICANDO DEPENDENCIAS PYTHON:"
PACKAGES=("requests" "elevenlabs" "opencv-python" "pillow" "tkinter")

for package in "${PACKAGES[@]}"; do
    if [ "$package" = "tkinter" ]; then
        python3 -c "import tkinter; print('✅ tkinter disponible')" 2>/dev/null || {
            echo "❌ tkinter no disponible"
            echo "   Instala con: sudo apt-get install python3-tk"
        }
    else
        python3 -c "import $package; print('✅ $package disponible')" 2>/dev/null || {
            echo "❌ $package no disponible"
            echo "   Instala con: pip install $package"
        }
    fi
done
echo ""

# Verificar archivo de video
echo "🎥 VERIFICANDO ARCHIVOS NECESARIOS:"
if [ -f "instrucciones.mp4" ]; then
    echo "✅ instrucciones.mp4 encontrado"
    echo "   Tamaño: $(du -h instrucciones.mp4 | cut -f1)"
else
    echo "❌ instrucciones.mp4 no encontrado"
    echo "   Este archivo es necesario para la experiencia"
fi
echo ""

# Ejecutar test de audio
echo "🎤 EJECUTANDO TEST DE AUDIO:"
if [ -f "test_audio.py" ]; then
    echo "✅ test_audio.py encontrado"
    echo "📞 Ejecutando test..."
    python3 test_audio.py
else
    echo "❌ test_audio.py no encontrado"
fi
echo ""

echo "🏁 VERIFICACIÓN COMPLETADA"
echo "=========================="
echo "💡 Si hay errores, sigue las instrucciones de instalación mostradas"
echo "💡 Para Raspberry Pi OS, también puedes necesitar:"
echo "   sudo raspi-config -> Advanced Options -> Audio -> Force 3.5mm jack"
echo "   sudo apt-get update && sudo apt-get upgrade"
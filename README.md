# nodo_2

Proyecto que graba audio con PyAudio y lo sube a ElevenLabs para clonación de voz.

## Raspberry Pi / Linux notes

Antes de instalar dependencias Python, instala PortAudio en Raspbian/Debian:

```bash
sudo apt update
sudo apt install -y libportaudio2 libportaudiocpp0 portaudio19-dev

# luego crear/activar virtualenv e instalar paquetes Python
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Notas:
- Si hay problemas con el micrófono, usa `arecord -l` para listar dispositivos y configura `input_device_index` en el script.
- El script usa `xdg-open` para abrir videos en Linux y `open` en macOS. En Raspberry Pi con entorno de escritorio `xdg-open` debería abrir el reproductor por defecto.
# nodo_2

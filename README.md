# Tarea 5 – Sistemas Operativos

**Autor:** @Cristian039
**Fecha:** Mayo 2025

---

## 🚗 Carro Seguidor de Línea (Tkinter + PID + Docker)

Este proyecto implementa un carro virtual que sigue una pista utilizando sensores simulados y un controlador PID. Usa Tkinter para mostrar la GUI y está preparado para correr en Docker, con opción de ser publicado en Docker Hub y alojado en GitHub.

### 🎥 Demostración en video

⚠️ GitHub no permite reproducción embebida de video directamente en el README. Sin embargo, si estás viendo este archivo desde una página web (como GitHub Pages), el video se reproducirá a continuación. Si no, arriba en los archivos aparecerá el video: entra y haz clic en "View Raw" para descargarlo y verlo.

### 📁 Estructura del proyecto

```
carro_seguidor_docker/
├── CarroFinal.py                 # Código fuente con el PID y GUI
├── Dockerfile                    # Imagen Docker para ejecutar con entorno gráfico
├── Video De Carrito Seguidor.mkv  # Video de demostración
└── README.md                     # Documentación del proyecto
```

### 🔧 Requisitos para ejecución local

* Python 3.10 o superior
* Tkinter instalado (incluido en la mayoría de distribuciones)
* Linux, Windows o WSL2 con entorno gráfico

### ▶️ Ejecución local

```bash
python CarroFinal.py
```

El programa abrirá una ventana con el carro recorriendo la pista. Está diseñado para seguir una línea negra sobre fondo claro.

### 🐳 Construcción y ejecución con Docker

#### 🔨 Construcción

```bash
docker build -t carro_gui .
```

#### 🚀 Ejecución (en Linux con GUI y X11)

```bash
xhost +local:root

docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  carro_gui
```

#### 🩟 En Windows con XServer (VcXsrv o X410)

```bash
docker run -it \
  -e DISPLAY=host.docker.internal:0.0 \
  --rm \
  carro_gui
```

### ☁️ Subir imagen a Docker Hub

```bash
docker login
docker tag carro_gui cristian039/carro-seguidor:latest
docker push cristian039/carro-seguidor:latest
```

### ⬇️ Descargar y ejecutar desde Docker Hub

```bash
docker pull cristian039/carro-seguidor:latest
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  cristian039/carro-seguidor
```

### 🧠 Características del código

* Simulación gráfica con sensores y ruedas
* Control PID con suavizado de movimiento
* Pista curva personalizada
* Parada en estaciones (ej. “Control”)
* Optimizado para entorno Docker + GUI

---

## 🌌 Juego Galaxy Rush (Pygame + Boss + Power-ups)

Se personalizó el juego base de naves espaciales con:

* Imágenes personalizadas para nave, enemigos, disparos y fondo.
* Aparición de jefe (boss alien verde) cuando se alcanza cierto puntaje.
* Sistema de power-ups: velocidad, disparo doble, disparo rápido.
* Sistema de puntuación, vidas, y colisiones.
* Juego contenedorizado y subido a Docker Hub.

### Docker:

```bash
docker pull cristian039/galaxy-rush:latest
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  cristian039/galaxy-rush
```

---

## 🧐 ROS (Robot Operating System) en Docker: Talker + Listener

Se construyó un ejemplo básico con:

* Nodo `talker.py`: publica mensajes "Hola desde ROS en Docker"
* Nodo `listener.py`: escucha y responde mostrando en consola
* Todo ejecutado sobre la imagen `ros:noetic` en Docker

### Ejecución paso a paso:

1. Correr contenedor con `talker` y `roscore`:

```bash
docker run -it --name tarea5 cristian039/ros-tarea5 ./start_talker.sh
```

2. En otra terminal, ejecutar el listener:

```bash
docker exec -it tarea5 bash -c "source /opt/ros/noetic/setup.bash && python3 listener.py"
```

3. Ver salida tipo:

```
[INFO]: Listener recibió: Hola desde ROS en Docker
```
### 🎥 Demostración en video

⚠️ GitHub no permite reproducción embebida de video directamente en el README. Sin embargo, si estás viendo este archivo desde una página web (como GitHub Pages), el video se reproducirá a continuación. Si no, arriba en los archivos aparecerá el video: entra y haz clic en "View Raw" para descargarlo y verlo, se llamara video de Ros, comprobacion.
---

## 🧑‍💻 Autor

Cristian039
Proyecto educativo desarrollado para la Tarea 5 del curso de Sistemas Operativos.
Incluye simulación gráfica, comunicación entre procesos y contenedores Docker aplicados a interfaces gráficas y robótica.

---
